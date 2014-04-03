#!/usr/bin/env python

# vim: set noai tabstop=4 shiftwidth=4 expandtab:

import logging
import sys
import textwrap
import pprint
import os
import difflib
import re
import types

import argparse
# Documented at:
#  * http://docs.python.org/2/library/argparse.html
#  * http://docs.python.org/2/howto/argparse.html
#  * http://pymotw.com/2/argparse/

import requests # documented at: http://docs.python-requests.org/
import json
import base64
from getpass import getpass

def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

def create_auth_header( user=None, passw=None ):

    """
    """

    if not user:
        username = raw_input( 'username: ' )

    if not passw:
        password = getpass( 'password: ' )

    base64string = base64.encodestring('%s:%s' % (username, password)).strip()

    return "Basic %s" %base64string

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("The file %s does not exist!"%arg)
    else:
       return open(arg,'r')  #return an open file handle

SSL_ROOT_CAS = None

def set_root_ca_bundle( location=None ):

    global SSL_ROOT_CAS

    default_locations = [ ]
    default_locations.append( '/etc/ssl/certs/ca-certificates.crt' ) # Debian default location
    default_locations.append( '/etc/ssl/certs/ca-bundle.crt') #Red Hat default location

    # Use location if specified
    if location:
        if os.path.exists( location ):
            SSL_ROOT_CAS = location
            return True
        else:
            print 'file does not exist: %s' %location
            sys.exit(1)

    # Search for OS default locations
    for l in default_locations:

        if os.path.exists( l ):

            SSL_ROOT_CAS = l
            return True

    # Fallback to python module supplied CA file
    SSL_ROOT_CAS = requests.certs.where()
    return False


# Using a session to persist certain parameters across requests
s = requests.Session()
auth_header = create_auth_header()
s.headers.update( { 'Authorization' : auth_header } )
s.timeout = 3.000
base_url = 'http://localhost:8000' # should be read from config file
base_url = 'https://dev.cmt.surfsara.nl' # should be read from config file
set_root_ca_bundle()

API_VERSION = '1'

full_url = '%s/api/v%s/' %( base_url, API_VERSION )

# Get a list of all existing entities in CMT
try:
    r = s.get(full_url, verify=SSL_ROOT_CAS)

except requests.exceptions.SSLError as ssl_err:
    print 'Unable to verify SSL certificate: %s' %str( ssl_err)
    print 'Using root CAs: %s' %ssl_root_cas
    print 'Are your ROOT CAs up2date?'
    sys.exit(1)

except requests.exceptions.ConnectionError as req_ce:
    print 'Error connecting to server: %s' % str( req_ce )
    sys.exit(1)

try:
    print '>>> REQUEST:', r
    assert(r.status_code == requests.codes.OK), 'HTTP response not OK'
except (AssertionError, requests.exceptions.RequestException), e:
    print 'Server gave HTTP response code %s: %s' % (r.status_code,r.reason)
    sys.exit(1)

ENTITIES = r.json().keys()

def query(s):
    """
    Build a query from a string like '<LH><OPER><RH>'
    If operand is '=', it returns the array [<LH>,<RH>]
    If operand is '-=', '+=', '<=', '>=' or '!=' it returns
    the same array, with the operand '-', '+', '<', '>' or '!'
    postfix appended
    >>> query('x=y')
    ['x', 'y']
    >>> query('x+=y')
    ['x', 'y', '+']
    """
    _s = s.split('=')
    if _s[0].endswith(('+', '-', '>', '<', '!')):
        oper = _s[0][-1]
        _s[0] = _s[0][:-1]
        _s.append(oper)
    return _s

def check_multiple_values( value ):

    if value.find( ',') == -1:

        return [ value ]

    return value.split(',')

MANY_FIELDS = { }

def get_many_fields( entity ):

    url = '%s/' % (full_url + entity)

    # Get a list of all existing entities in CMT
    try:
        r = s.get(url, verify=SSL_ROOT_CAS)
    except requests.exceptions.ConnectionError as req_ce:
        print 'Error connecting to server: %s' % req_ce.args[0].reason.strerror
        sys.exit(1)

    try:
        print '>>> REQUEST:', r
        assert(r.status_code == requests.codes.OK), 'HTTP response not OK'
    except (AssertionError, requests.exceptions.RequestException), e:
        print 'Server gave HTTP response code %s: %s' % (r.status_code,r.reason)
        sys.exit(1)

    for field_name, field_value in r.json()['results'][0].items():

        if type( field_value ) is types.ListType:

            if not MANY_FIELDS.has_key( entity ):

                MANY_FIELDS[ entity ] = [ ]

            if not field_name in MANY_FIELDS[ entity ]:

                MANY_FIELDS[ entity ].append( field_name )

ENTITIES = r.json().keys()

def args_to_payload(entity, q):
    """

    >>> args_to_payload([['cluster__name', 'cluster1'], ['rack__label', 'rack1']])
    {'rack__label': 'rack1', 'cluster__name': 'cluster1'}
    """
    d = {}
    for stmt in q:
        if MANY_FIELDS.has_key( entity ):
            if stmt[0] in MANY_FIELDS[ entity ]:
                d[stmt[0]] = check_multiple_values( stmt[1] )
            else:
                d[stmt[0]] = stmt[1]
        else:
            d[stmt[0]] = stmt[1]
    return d


class Client:

#    class ReadAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string=None):
#            print '>>> %r :: %r :: %r' % (namespace, values, option_string)
#            setattr(namespace, self.dest, values)
#            #print '... readparser:', readparser


    def get_related_ent(self, entity, field):
        """
        Current implementation is a placeholder. This must be implemented server-side.
        """
        print 'LOOKING UP ENTITY FOR %s__%s' % (entity, field)
        if entity == 'equipment':
            if field == 'cluster':
                return 'clusters'
            elif field == 'rack':
                return 'racks'
        return None


    def create(self, args):

        print '>>> <CREATING>'
        # Be sure there's a --set arg before taking care of the rest of the args
        try:
            assert(args['set']), 'Missing --set arguments'
        except AssertionError, e:
            print AssertionError, e

        # Prepare POST request (r) based on session (s) and given --set args
        entity = args['entity'].pop()
        get_many_fields( entity )

        url = '%s/' % (full_url + entity)
        payload = args_to_payload(entity, args['set'])
        print 'PAYLOAD:', payload


        s.headers.update( {'content-type': 'application/json' } )
        try:
            r = s.post(url, data=json.dumps(payload), verify=SSL_ROOT_CAS) 
        except ConnectionError, e:
            print 'Error connecting to server: %s' % e

        print '>>> </CREATING>'
        return r.json()

    def read(self, args, lookup=False):

        print '>>> <READING>'
        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), 'Missing --get arguments'
        except AssertionError, e:
            print AssertionError, e

        # Prepare GET request (r) based on session (s) and given --get args
        entity = args['entity'].pop()
        url = '%s/' % (full_url + entity)
        payload = args_to_payload(entity, args['get'])

        if args.has_key( 'fields' ):
            if args['fields'] != None:
                payload[ 'fields' ] = args['fields'][0]

        print 'PAYLOAD:', payload

        s.headers.update( {'content-type': 'application/json' } )
        r = s.get(url, params=payload, verify=SSL_ROOT_CAS)

        # Check for HTTP-status 200
        try:
            assert(r.status_code == requests.codes.OK), 'HTTP response not OK'
        except AssertionError, e:
            print 'Server gave HTTP response code %s: %s' % (r.status_code,r.reason)

        # Return response in JSON-format
        try:
            assert(r.json()), 'JSON decoding failed'
        except ValueError, e:
            print ValueError, e
            return None
        print '>>> </READING>'

        if lookup:
            print r.json()
        return r.json()


    def update(self, args):

        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), 'Missing --get arguments'
        except AssertionError, e:
            print AssertionError, e

        # Be sure there's a --set arg before taking care of the rest of the args
        try:
            assert(args['set']), 'Missing --set arguments'
        except AssertionError, e:
            print AssertionError, e

        # Get data from given --get args to prepare a request
        entity = args['entity'].pop()
        url = '%s/' % (full_url + entity )
        payload = args_to_payload(entity, args['get'])
        s.headers.update( {'content-type': 'application/json' } )
        response = s.get(url, params=payload, verify=SSL_ROOT_CAS)

        # Return response in JSON-format
        try:
            assert(r.json()), 'JSON decoding failed'
        except ValueError, e:
            print ValueError, e
            return None

        pprint.pprint( response.json() )

        response_data = response.json()

        result_count = response_data[ 'count' ]

        if result_count == 0:

            print 'No objects found'
            return 

        confirm_str = 'You are about to update: %s object(s). Are you sure ([N]/Y)?: ' %result_count
        confirm = raw_input( confirm_str )
      
        if confirm.lower() != 'y':

            return

        get_many_fields( entity )

        payload = args_to_payload(entity, args['set'])

        for result in response_data['results']:

            print 'URL:', result['url']
            print 'PAYLOAD:', payload
            reponse = s.patch(result['url'], data=json.dumps(payload), verify=SSL_ROOT_CAS )

            # Return response in JSON-format
            try:
                assert(response.json()), 'JSON decoding failed'
            except ValueError, e:
                print ValueError, e
                return None

            #pprint.pprint( response.json() )

    def delete(self, args):
        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), 'Missing --get arguments'
        except AssertionError, e:
            print AssertionError, e

        # Get data from given --get args to prepare a request
        entity = args['entity'].pop()
        url = '%s/' % (full_url + entity )
        payload = args_to_payload(entity, args['get'])
        s.headers.update( {'content-type': 'application/json' } )
        response = s.get(url, params=payload, verify=SSL_ROOT_CAS)

        # Return response in JSON-format
        try:
            assert(r.json()), 'JSON decoding failed'
        except ValueError, e:
            print ValueError, e
            return None

        pprint.pprint( response.json() )

        response_data = response.json()

        result_count = response_data[ 'count' ]

        if result_count == 0:

            print 'No objects found'
            return 

        confirm_str = 'You are about to delete: %s object(s). Are you sure ([N]/Y)?: ' %result_count
        confirm = raw_input( confirm_str )
      
        if confirm.lower() != 'y':

            return

        for result in response_data['results']:

            print 'URL:', result['url']

            reponse = s.delete(result['url'], verify=SSL_ROOT_CAS)

            # Return response in JSON-format
            try:
                assert(response.json()), 'JSON decoding failed'
            except ValueError, e:
                print ValueError, e
                return None

            #pprint.pprint( response.json() )
 
    # Parse a template
    def parse(self, args):
        print '>>> <PARSING>'

        # Prepare POST request (r) based on session (s)
        url = full_url + 'template'

        payload = {}

        file_obj = args['template'][0]
        filename = file_obj.name

        files = { 'file' : file_obj }

        print 'Sending template to server and awaiting response..'

        response = s.post(url, params=payload, files=files, verify=SSL_ROOT_CAS )

        # Return response in JSON-format
        try:
            assert(response.json()), 'JSON decoding failed'
        except ValueError, e:
            print ValueError, e
            return None

        file_obj.close()

        output_ignore_regexps = [ ]

        prompt_write = False

        for output_filename, output_file_attrs in response.json().items():

            output_file_contents = output_file_attrs['contents']
            output_file_diff_ignore = output_file_attrs['diff_ignore']

            print 'Received output file: %s' %output_filename
            print '- file size: %d' %len( output_file_contents )

            #pprint.pprint( output_file_contents )

            #pprint.pprint( output_file_diff_ignore )

            for regex in output_file_diff_ignore:

                output_ignore_regexps.append( re.compile( regex ) )

            if os.path.isfile( output_filename ):

                prompt_write = True

                print "file already exists: %s" %output_filename

                if not os.access( output_filename, os.R_OK ):

                    print "cannot read original file (permission denied): %s" %output_filename
                    print "cannot check diff between original file and new output file"

                else:

                    original_file = open( output_filename, 'r' )
                    original_contents = original_file.readlines()
                    original_file.close()

                    #pprint.pprint( original_contents )

                    output_list_contents = splitkeepsep( output_file_contents, '\n' )

                    if output_list_contents[-1] == '':

                        # last \n will result in extra list element containing nothing
                        del output_list_contents[-1]

                    #pprint.pprint( output_list_contents )

                    diff_check_new = output_list_contents[:]

                    for l in xrange( len(diff_check_new) - 1, -1, -1 ):

                        for r in output_ignore_regexps:

                            if r.match( diff_check_new[l] ):

                                del diff_check_new[l]

                    diff_check_org = original_contents[:]

                    for l in xrange( len(diff_check_org) - 1, -1, -1 ):

                        for r in output_ignore_regexps:

                            if r.match( diff_check_org[l] ):

                                del diff_check_org[l]

                    udiff = difflib.unified_diff( diff_check_org, diff_check_new )

                    udiff_list = list( udiff )

                    if len( udiff_list ) > 0:

                        print 'Received (new) output contents differs from original contents for file: %s' %output_filename
                        want_diff = raw_input( "Would you like to see the diff(erence)? ([N/y]): " )

                        if want_diff.lower() == 'y':

                            udiff = difflib.unified_diff( original_contents, output_list_contents, fromfile=output_filename, tofile=output_filename )

                            #udiff_list = list( udiff )

                            for uline in udiff:

                                print uline,

                    else:
                        print 'no difference (excluding commented lines) with original'

        if prompt_write:

            really_write = raw_input('Really write these output files? ([N/y]): ')

            if really_write.lower() != 'y':

                print "Doing nothing and exiting.."
                return True

        for output_filename, output_file_attrs in response.json().items():

            output_file_contents = output_file_attrs['contents']

            target_dir = os.path.dirname( output_filename )

            if not os.path.isdir( target_dir ):

                print "Directory '%s' for output file '%s' does not exist" %( target_dir, output_filename )

                if not os.access( target_dir, os.W_OK ):

                    print "I do not have permission to create the directory"
                    print "Aborting and doing nothing.."
                    sys.exit(1)

                want_create_dir = raw_input( "You want me to create the directory? ([N/y]): " )

                if want_create_dir.lower() == 'y':

                    print "creating directory: %s" %target_dir
                    os.makedirs( target_dir )

                else:

                    print "skipping output file: %s" %output_filename
                    continue

            if os.path.isfile( output_filename ) and not os.access( output_filename, os.W_OK ):

                print "Permission denied, file is not writeable: %s" %output_filename
                print "skipping output file: %s" %output_filename
                continue

            print "writing '%s': " %output_filename,
            f = open(output_filename, 'w')
            f.writelines(output_file_contents)
            f.close()
            print 'done'

        return True

    # Fire a request to the server
    def request(server, r):
        pass


    def __init__(self, args):

        print '>>> Initializing client with args:', args
        _args = None

        output_formats = (
            'plain',
            'xml',
            'json',
            # TODO: complete list
        )

        # Initialize a parser to parse the given arguments
        parser = argparse.ArgumentParser(
            description=textwrap.dedent(
                """\
                This is the CMT client application.
                It's friends with the CMT server, and likes to talk with it.
                """
            ),
            epilog="That's all folks!"
        )

        # TODO: implement
        parser.add_argument('--dry-run', '-n', action='store_true', dest='dryrun', help='do a dry run')
        output_group = parser.add_mutually_exclusive_group()
        output_group.add_argument('--verbose', '-v', action='count', default=0, help='increase output verbosity')
        output_group.add_argument('--quiet', '-s', action='store_true', help='suppress output messages')
        parser.add_argument('--version', action='version', version='%(prog)s 2.0')


        getparser = argparse.ArgumentParser(add_help=False)
        getparser.add_argument('--get', nargs='+', metavar='QUERY', type=query, help='Query to match existing objects, like "KEY=VAL"')
        setparser = argparse.ArgumentParser(add_help=False)
        setparser.add_argument('--set', nargs='+', metavar='ASSIGNMENT', type=query, help='Definition to assign values to fields, like "KEY=VAL"')
        fieldsparser = argparse.ArgumentParser(add_help=False)
        fieldsparser.add_argument('--fields', nargs='+', metavar='FIELDS', type=str, help='Comma seperated list of fields to get, like "KEY[,KEY]"')

        # CRUD commands to [C]reate, [R]ead, [U]pdate and [D]elete objects are parsed by subparsers.
        # Same applies for parsing of templates.
        subparsers = parser.add_subparsers(description=textwrap.dedent(
            """\
            These subcommands should be used for CRUD-actions and template-parsing.
            """
            ),
            dest='command', # to store the name of the subparser that was invoked
            help='Available actions')

        # CRUD command Create
        create_parser = subparsers.add_parser('create', help='Create a new object', parents=[setparser])
        create_parser.add_argument('entity', choices=ENTITIES, nargs=1, help='The entity to create')
        create_parser.set_defaults(func='create')

        # CRUD command Read
        read_parser = subparsers.add_parser('read', help='Read an existing object', parents=[getparser,fieldsparser])
        read_parser.add_argument('entity', choices=ENTITIES, nargs=1, help='The entity to read')
        read_parser.set_defaults(func='read')

        # CRUD command Update
        update_parser = subparsers.add_parser('update', help='Update an existing object', parents=[getparser,setparser])
        update_parser.add_argument('entity', choices=ENTITIES, nargs=1, help='The entity to update')
        update_parser.set_defaults(func='update')

        # CRUD command Delete
        delete_parser = subparsers.add_parser('delete', help='Delete an existing object', parents=[getparser])
        delete_parser.add_argument('entity', choices=ENTITIES, nargs=1, help='The entity to delete')
        delete_parser.set_defaults(func='delete')

        # Command for parsing of templates
        parse_parser = subparsers.add_parser('parse', help='Parse a CMT template')
        parse_parser.set_defaults(func='parse')
        file_group = parse_parser.add_argument_group('files', 'Arguments used for input and output')
        file_group.add_argument('template', type=lambda x: is_valid_file(parse_parser,x), nargs=1, help='The template file to parse')
        file_group.add_argument('--output', '-o', metavar='FILE', type=file, nargs=1, help='Overwrite output destination')



        try:
            self._args = vars(parser.parse_args())
            print '>>> PARSED ARGS:', self._args
            #if self._args['func'] == 'create':
            #    if not self._args['assign']:
            #        print "Can't create object(s) without a valid QUERY to match for or ASSIGNMENT to assign."
            #elif self._args['func'] == 'read':
            #    if not self._args['matching']:
            #        parser.error("Can't read object(s) without a valid QUERY to match for.")
            #        print "Can't read object(s) without a valid QUERY to match for."
            #elif self._args['func'] == 'update':
            #    if not self._args['matching'] or not self._args['assign']:
            #        print "Can't update object(s) without a valid QUERY to match for or ASSIGNMENT to assign."
            #elif self._args['func'] == 'delete':
            #    if not self._args['matching']:
            #        print "Can't delete object(s) without a valid QUERY to match for."
        except AttributeError, e:
            print 'Invalid entity given'
        except NameError, e:
            print 'nameerror', e



def main(args):
    try:
        c = Client(args)
        parsed_args = c._args
        #print '>>> PARSER:', parsed_args
       
 
        # Route parsed args to the action given on command line
        command = parsed_args['func']
        if command == 'read':
            json = c.read(parsed_args)
            pprint.pprint(json)
        elif command =='create':
            json = c.create(parsed_args)
            pprint.pprint(json)
        elif command == 'update':
            c.update(parsed_args)
        elif command == 'delete':
            c.delete(parsed_args)
        elif command == 'parse':
            c.parse(parsed_args)

        return 1
    except SystemExit:
        return 2
    #except:
    #    print '>>> Error:', sys.exc_info()[0]
    #    return -1


if __name__ == '__main__':
    status = main(sys.argv[1:])
    print '>>> exit-status:', status
    sys.exit(status)
