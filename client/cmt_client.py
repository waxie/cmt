#!/usr/bin/env python
#
# This file is part of CMT
#
# CMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# CMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMT.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2012-2017 SURFsara
#
# Why did you not use the requests module, well. With this version of the
# client you only need to have Python (we could run this on our switches)
#
'''
This is the api client tool for the cmt server
'''

import argparse
import cookielib
import urllib2
import os
import getpass
import re
import sys
import urlparse
import urllib
import json
import itertools
import mimetools
import mimetypes
import difflib
import subprocess

## START CONFIG
CMT_SERVER = ''
CMT_INVENTORY = {}
CMT_API_VERSION = ''
CMT_TEMPLATEDIR = ''
## END CONFIG


class ClientAuthException(Exception):
    pass


class ClientException(Exception):
    pass


class MultiPartForm(object):

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [part_boundary,
             'Content-Disposition: form-data; name="%s"' % name,
             '',
             value,
             ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [part_boundary,
             'Content-Disposition: file; name="%s"; filename="%s"' % \
             (field_name, filename),
             'Content-Type: %s' % content_type,
             '',
             body,
             ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)


class Client(object):

    methods = ['GET', 'POST', 'UPDATE', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH']
    realm_matcher = re.compile(r'^Basic realm\=\"(.+)\"$')
    auth_tries = 0
    max_auth_tries = 3

    def __init__(self, username=None, password=None):

        if __name__ == '__main__':
            self.as_module = False
        else:
            self.as_module = True

        self.uri = CMT_SERVER
        self.username = username
        self.password = password
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie)
        )
        self.opener.addheaders = [
            ('User-agent', 'CmtClient/%s' % CMT_API_VERSION),
            ('Accept', 'application/json')
        ]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__disconnect()

    def request(self, method, cmt_object, get_args=None, set_args=None):

        if method == 'read':
            http_method = 'GET'
        elif method == 'update':
            http_method = 'PUT'
        elif method == 'create':
            http_method = 'POST'
        elif method == 'delete':
            http_method = 'DELETE'
        elif method == 'parse':
            http_method = 'POST'

        if cmt_object not in CMT_INVENTORY:
            raise ClientException('Given object %s is not a valid CMT object')
        path = CMT_INVENTORY[cmt_object]['url']
        url = urlparse.urljoin(self.uri, path)

        if get_args:
            get_args = urllib.urlencode(self.__create_query(get_args))
        if set_args:
            set_args = self.__create_query(set_args)

        # This does not work yet, need to update the backend for this
        if http_method in ['DELETE', 'PUT']:
            result = {
                'count': 0,
                'next': None,
                'previous': None,
                'results': list()
            }
            t_result = self.__request(url, 'GET', args_get=get_args, args_post=None)

            if t_result and 'count' in t_result and t_result['count'] > 0:

                for tr in t_result['results']:
                    if http_method == 'PUT':
                        get_args = None

                        for key, value in tr.items():
                            if key in ['url', 'created_on', 'updated_on']:
                                continue
                            if not value:
                                continue

                            if key not in set_args:
                                set_args[key] = value
                        set_args = urllib.urlencode(set_args)
                    else:
                        get_args = None
                        set_args = None

                    tr_result = self.__request(tr['url'], http_method, args_get=get_args, args_post=set_args)

                    if method.lower() == 'delete':
                        tr_result.update(tr)
                        result['results'].append(tr)
                    else:
                        result['results'].append(tr_result)
                    result['count'] += 1
        else:
            if set_args and cmt_object != 'template':
                set_args = urllib.urlencode(set_args)
            elif set_args:
                form = MultiPartForm()

                if 'files' not in set_args:
                    raise ClientException('Invalid format given for parse method')
                for key, value in set_args['files'].items():
                    form.add_file('file', os.path.basename(value.name), value)
                set_args = form

            result = self.__request(url, http_method, args_get=get_args, args_post=set_args)
        return result

    def __query(self, s):
        _s = s.split('=')
        if _s[0].endswith(('+', '-', '>', '<', '!')):
            oper = _s[0][-1]
            _s[0] = _s[0][:-1]
            _s.append(oper)
        return _s



    def __create_query(self, args):
        r_args = dict()

        for arg in args:
            pair = self.__query(arg)
            if len(pair) != 2 and len(pair) != 3 and pair[2] not in ['+', '-', '>', '<', '!']:
                raise ClientException('Given query is wrong')

            r_args[pair[0]] = pair[1]
        return r_args

    def __auth_header(self, error, uri, method, args_get, args_post):
        if self.auth_tries > self.max_auth_tries:
            raise ClientAuthException('To many authentication failures')
        self.auth_tries += 1

        if self.as_module and not self.username and not self.password:
            raise ClientAuthException('When using as module, please initiate class with username and password')

        while not self.username:
            self.username = raw_input('Username [%s]: ' % os.getlogin())
            if not self.username:
                self.username = os.getlogin()

        while not self.password:
            self.password = getpass.getpass('Password: ')

        realm_header = error.headers.get('WWW-Authenticate', None)

        if realm_header:
            realm_found = self.realm_matcher.findall(realm_header)
            if len(realm_found) > 1:
                raise ClientAuthException('Unable to determine realm name')
            elif realm_found and len(realm_found) < 1:
                realm_found = None
            else:
                realm_found = realm_found[0]
        else:
            realm_found = False

        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm_found, uri, self.username, self.password)
        self.opener.add_handler(auth_handler)
        return self.__request(uri, method=method, args_get=args_get, args_post=args_post)

    def __request(self, uri, method='GET', args_get=None, args_post=None):

        if method.upper() not in self.methods:
            raise ClientException('Given method is invalid choose from: %s' % ', '.join(method.upper()))
        json_data = dict()

        try:
            if args_post and type(args_post) is MultiPartForm:
                request = urllib2.Request(uri)
                body = str(args_post)
                request.add_header('Content-Length', len(body))
                for line in body.splitlines():
                    if line.startswith('Content-'):
                        parts = [ x.strip() for x in line.split(':') ]
                        request.add_header(parts[0], ';'.join(parts[1:]))
                request.add_data(body)
            elif args_get:
                request = urllib2.Request('%s?%s' % (uri, args_get))
            elif args_post:
                request = urllib2.Request(uri, data=args_post)
            elif args_get and args_post:
                request = urllib2.Request('%s?%s' % (uri, args_get), data=args_post)
            else:
                request = urllib2.Request(uri)

            request.get_method = lambda: method
            data = self.opener.open(request)

            if method in ['DELETE']:
                json_data = dict()
            else:
                json_data = json.loads(data.read())
            json_data['response'] = '%d - %s' % (data.getcode(), data.msg)
        except urllib2.HTTPError as error:
            ## Retry with authentication header
            if error.code in [401]:
                return self.__auth_header(error, uri, method, args_get, args_post)
            ## Just quit and show the error
            else:
                data = error.read()
                json_data = json.loads(data)
                json_data['response'] = '%d - %s' % (error.code, error.msg)
        ## When the server is bad
        except ValueError as error:
            raise ClientException('return data is not valid json')

        return json_data

    def __disconnect(self):
        self.opener.close()

    def __del__(self):
        self.__disconnect()


def generate_index(string):
    # Is used to generate a index, this way we can also sort nummeric values in a string
    return [int(y) if y.isdigit() else y for y in re.split(r'(\d+)', string)]


def choose_file(action, choices):

    p('Choose a file:')
    for choice in choices:
        p('  %-2d: %s' % (choices.index(choice)+1, choice))
    chosen_number = input('Choose: ')

    if chosen_number > len(choices) or chosen_number < 1:
        raise argparse.ArgumentError(action, 'Invalid number chosen')

    return choices[chosen_number-1]


class FieldCheck(argparse.Action):
    # Todo: need to support django __ query language

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string == '--get':
            action = namespace.get
        elif option_string == '--set':
            action = namespace.set
        else:
            action = None

        if namespace.cmt_object not in CMT_INVENTORY:
            raise argparse.ArgumentError(action, 'Something went wrong badly, unable to find model %s' % namespace.cmt_object)

        for value in values:
            pair = value.split('=')

            if len(pair) != 2:
                raise argparse.ArgumentError(action, 'option must be specified as <select>=<value>. ie label=r2n1')

            field_name = pair[0].rstrip('!-+<>').split('__')[0]
            if field_name not in CMT_INVENTORY[namespace.cmt_object]['fields']:
                raise argparse.ArgumentError(action, 'Invalid field choose from: %s' %(
                    ', '.join(CMT_INVENTORY[namespace.cmt_object]['fields'])
                ))

        setattr(namespace, self.dest, values)


class TemplatefileCheck(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        if values and os.path.exists(values) and os.access(values, os.R_OK):
            a_file = os.path.realpath(values)
        elif values and os.path.exists(values) and not os.access(values, os.R_OK):
            raise argparse.ArgumentError(namespace.filename, 'unable to read specified file, check permissions')
        elif values and not os.path.exists(values):
            raise argparse.ArgumentError(namespace.filename, 'unable to find specified file')
        else:
            template_files = list()
            for tfile in sorted(os.listdir(CMT_TEMPLATEDIR), key=generate_index):
                if tfile.endswith('.cmt'):
                    template_files.append(tfile)

            a_file = os.path.join(CMT_TEMPLATEDIR, choose_file(namespace.filename, template_files))

            if not os.access(a_file, os.R_OK):
                raise argparse.ArgumentError(namespace.filename, 'unable to read specified file, check permissions')
            elif not os.path.exists(a_file):
                raise argparse.ArgumentError(namespace.filename, 'unable to find specified file')

        setattr(namespace, self.dest, a_file)


def color_diff(diff):
    COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ],
            list(range(30, 38))
        ))
    )
    RESET = '\033[0m'

    for line in diff:
        if line.strip().startswith('+'):
            p(color(line.strip(), 'green'))
        elif line.strip().startswith('-'):
            p(color(line.strip(), 'red'))
        elif line.strip().startswith('^'):
            p(color(line.strip(), 'blue'))
        else:
            p(line.strip())


def color(s, color='grey'):
    COLORS = dict(
        list(zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ],
            list(range(30, 38))
        ))
    )
    RESET = '\033[0m'

    if color not in COLORS:
        raise ClientException('Chosen color %s does not exist, choose from %s' % (color, ','.join(COLORS.keys())))

    return '\033[%dm' % COLORS[color] + s + RESET


def p(*args, **kwargs):

    try:
        Print = eval('print')
        Print(*args, **kwargs)
    except SyntaxError:
        try:
            D = dict()
            exec('from __future__ import print_function\np=print', D)
            D['p'](*args, **kwargs)
            del D
        except SyntaxError:
            raise ClientException('Please upgrade your Python version to 2.6 or higher')


def args_parser():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Enable dry-run, also enables verbose mode')
    parser.add_argument('--version', action='version', version='CMT Client API version: %s, host: %s' % (CMT_API_VERSION, CMT_SERVER))

    subparsers = parser.add_subparsers()

    valid_objects = [x for x in CMT_INVENTORY.keys() if x != 'template']

    read_parser = subparsers.add_parser('read', help='Fetch and object from CMT')
    read_parser.add_argument('cmt_object', help='What type of data', choices=valid_objects)
    read_parser.add_argument('--get', nargs='+', help='This is your query', action=FieldCheck, required=True)
    read_parser.set_defaults(mode='read')

    create_parser = subparsers.add_parser('create', help='Create an object in CMT')
    create_parser.add_argument('cmt_object', help='What type of data', choices=valid_objects)
    create_parser.add_argument('--set', nargs='+', help='Set the values', action=FieldCheck, required=True)
    create_parser.set_defaults(mode='create')

    update_parser = subparsers.add_parser('update', help='Update an object from CMT')
    update_parser.add_argument('cmt_object', help='What type of data', choices=valid_objects)
    update_parser.add_argument('--get', nargs='+', help='This is your query', action=FieldCheck, required=True)
    update_parser.add_argument('--set', nargs='+', help='Set the values', action=FieldCheck, required=True)
    update_parser.set_defaults(mode='update')

    delete_parser = subparsers.add_parser('delete', help='Delete an object from CMT')
    delete_parser.add_argument('cmt_object', help='What type of data', choices=valid_objects)
    delete_parser.add_argument('--get', nargs='+', help='This is your query', action=FieldCheck, required=True)
    delete_parser.set_defaults(mode='delete')

    parse_parser = subparsers.add_parser('parse', help='Parse a template from CMT')
    parse_parser.add_argument('filename', help='Specify the templatefile, leave empty for menu', nargs='?', action=TemplatefileCheck)
    parse_parser.add_argument('-w', '--write', help='Do not ask to write, just write', action='store_true')
    parse_parser.add_argument('-d', '--skip-diff', help='Do not ask to show the diff', action='store_true')
    parse_parser.add_argument('-e', '--skip-epilogue', help='Skip epilogue', action='store_true')
    parse_parser.set_defaults(mode='parse')

    return parser.parse_args()


if __name__ == '__main__':

    try:
        args = args_parser()
        client = Client()
        result = None

        if args.mode in ['read', 'delete']:
            result = client.request(args.mode, args.cmt_object, args.get, None)
        elif args.mode in ['update']:
            result = client.request(args.mode, args.cmt_object, args.get, args.set)
        elif args.mode in ['create']:
            result = client.request(args.mode, args.cmt_object, None, args.set)
        elif args.mode in ['parse']:
            t_args = {
                'files': {
                    'file': open(args.filename, 'rb')
                }
            }
            result = client.request(args.mode, 'template', None, t_args)

        if result and args.mode != 'parse':
            p('[%s] Result:' % args.mode.upper())
            p(
                json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
            )
        elif result:
            if 'error' in result:
                raise ClientException(result['error'])

            data = json.loads(result)
            write_files = list()
            for store_file, contents in data['files'].items():
                path = os.path.dirname(store_file)

                if not os.path.isdir(path):
                    raise ClientException('Unable to save file directory %s does not exist' % path)
                if not os.access(path, os.W_OK):
                    raise ClientException('You don\'t have permission to store files at %s' % path)

                if os.path.isfile(store_file) and not os.access(store_file, os.W_OK):
                    raise ClientException('File already exists and you don\'t have permission to edit file %s' % store_file)

                if os.path.isfile(store_file):

                    with open(store_file, 'r') as fi:
                        current_file_contents = fi.readlines()

                    d = difflib.unified_diff(
                        current_file_contents, contents.splitlines(1),
                        fromfile=store_file, tofile=store_file, lineterm='')
                    diff = list(d)

                    if len(diff) > 0:
                        write_files.append(store_file)
                        if not args.skip_diff:
                            p('[DIFF] File %s has changed, do you want to view the diff (y/N): ' % store_file, end='')
                            yes_or_no = raw_input()
                            if yes_or_no in ['y', 'Y']:
                                color_diff(diff)
                else:
                    write_files.append(store_file)
                    

            if not args.write and write_files:
                p('[WRITE] Do you want to save the changes (y/N: ', end='')
                yes_or_no = raw_input()
                if yes_or_no in ['y', 'Y']:
                    args.write = True

            if args.write and write_files:
                for wfile in write_files:
                    with open(wfile, 'w') as fo:
                        fo.write(data['files'][wfile])
            elif not args.write and write_files:
                p('[WRITE] Skipped writing changes to disk')
   
            if args.write and not args.skip_epilogue and write_files:
                for epilogue in data['epilogue']:
                    p('[EPILOGUE] Running command: %s' % epilogue.strip())
                    p = subprocess.Popen(epilogue.strip(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
           
                    stdout, stderr = p.communicate()
           
                    if stdout:
                        p(stdout)
                   
                    if p.returncode != 0:
                        p('  An error has occured, exit code %d' % p.returncode)
                 
                    if stderr:
                        p(stderr, file=sys.stderr)
            elif not write_files:
                p('[EPILOGUE] Files are not changed, not running epilogue')
            elif write_files and not args.write:
                p('[EPILOGUE] Changed files are not written to disk, not running epilogue')
                
    except ClientException as error:
        p('[ERROR] An error has occured: %s' % str(error), file=sys.stderr)
    except ClientAuthException as error:
        p('[ERROR] Unable to authenticate: %s' % str(error), file=sys.stderr)
    except KeyboardInterrupt as error:
        p('\n\nCaught Ctrl+C, exit %s' % sys.argv[0])
