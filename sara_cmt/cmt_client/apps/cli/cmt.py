#!/usr/bin/env python

import logging
import sys
import textwrap
import pprint

import argparse
# Documented at:
#  * http://docs.python.org/2/library/argparse.html
#  * http://docs.python.org/2/howto/argparse.html
#  * http://pymotw.com/2/argparse/

import requests # documented at: http://docs.python-requests.org/
import json
import base64
from getpass import getpass


def create_auth_header():

    """
    """

    username = raw_input( 'username: ' )
    password = getpass( 'password: ' )

    base64string = base64.encodestring('%s:%s' % (username, password)).strip()

    return "Basic %s" %base64string

# Decorator for debugging
def breadcrumbs(f):
    def _inner(*args, **kwargs):
        print "<%s>" % f.__name__.upper()
        f(*args, **kwargs)
        print "</%s>" % f.__name__.upper()
    return _inner


# Using a session to persist certain parameters across requests
s = requests.Session()
auth_header = create_auth_header()
s.headers.update( { 'Authorization' : auth_header } )
s.timeout=3.000

# Get a list of all existing entities in CMT
base_url = 'http://localhost:8000/' # should be read from config file
r = s.get(base_url)
try:
    ENTITIES = r.json().keys()
    assert(r.status_code == requests.codes.OK), 'HTTP response not OK'
except (AssertionError, requests.exceptions.RequestException), e:
    print 'Server gave HTTP response code %s: %s' % (r.status_code,r.reason)
    sys.exit(1)


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

def args_to_payload(q):
    """

    >>> args_to_payload([['cluster__name', 'cluster1'], ['rack__label', 'rack1']])
    {'rack__label': 'rack1', 'cluster__name': 'cluster1'}
    """
    d = {}
    for stmt in q:
        d[stmt[0]] = stmt[1]
    return d


class Client:

#    class ReadAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string=None):
#            print '>>> %r :: %r :: %r' % (namespace, values, option_string)
#            setattr(namespace, self.dest, values)
#            #print '... readparser:', readparser


    def create(self, args):

        # Be sure there's a --set arg before taking care of the rest of the args
        try:
            assert(args['set']), 'Missing --set arguments'
        except AssertionError, e:
            print AssertionError, e

        url = '%s/' % (base_url + args['entity'].pop())
        payload = args_to_payload(args['set'])
        s.headers.update( {'content-type': 'application/json' } )
        response = s.post(url, data=json.dumps(payload)) 

        try:
            assert(r.status_code == requests.codes.OK), 'HTTP response not OK'
        except AssertionError, e:
            print 'Server gave HTTP response code %s: %s' % (r.status_code,r.reason)

        return response.json()


    def read(self, args):

        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), 'Missing --get arguments'
        except AssertionError, e:
            print AssertionError, e

        # Get data from given --get args to prepare a request
        url = '%s/' % (base_url + args['entity'].pop())
        payload = args_to_payload(args['get'])
        s.headers.update( {'content-type': 'application/json' } )
        response = s.get(url, params=payload)

        # Return response in JSON-format
        try:
            assert(r.json()), 'JSON decoding failed'
        except ValueError, e:
            print ValueError, e
            return None
        return response.json()


    def update(self, args):
        # First get the selection of objects to update
        selection = read(args)
        print selection
        return


    def delete(self, args):
        print args
        return


    # Parse a template
    def parse(args):
        print args
        return


    @breadcrumbs
    # Fire a request to the server
    def request(server, r):
        pass


    #@breadcrumbs
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
        read_parser = subparsers.add_parser('read', help='Read an existing object', parents=[getparser])
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
        file_group = parse_parser.add_argument_group('files', 'Arguments used for input and output')
        file_group.add_argument('template', type=file, nargs=1, help='The template file to parse')
        file_group.add_argument('--output', '-o', metavar='FILE', type=file, nargs=1, help='Overwrite output destination')



        try:
            self._args = vars(parser.parse_args())
            print '>>> PARSED ARGS:', self._args
            if self._args['func'] == 'create':
                if not self._args['assign']:
                    print "Can't create object(s) without a valid QUERY to match for or ASSIGNMENT to assign."
            elif self._args['func'] == 'read':
                if not self._args['matching']:
                    parser.error("Can't read object(s) without a valid QUERY to match for.")
                    print "Can't read object(s) without a valid QUERY to match for."
            elif self._args['func'] == 'update':
                if not self._args['matching'] or not self._args['assign']:
                    print "Can't update object(s) without a valid QUERY to match for or ASSIGNMENT to assign."
            elif self._args['func'] == 'delete':
                if not self._args['matching']:
                    print "Can't delete object(s) without a valid QUERY to match for."
        except:
            pass



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
            c.create(parsed_args)
        elif command == 'delete':
            c.create(parsed_args)
        elif command == 'parse':
            c.create(parsed_args)

        return 1
    except SystemExit:
        return 2
    except:
        print '>>> Error:', sys.exc_info()[0]
        return -1


if __name__ == '__main__':
    status = main(sys.argv[1:])
    print '>>> exit-status:', status
    sys.exit(status)
