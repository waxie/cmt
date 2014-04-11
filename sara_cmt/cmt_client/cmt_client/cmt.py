#!/usr/bin/env python

# vim: set noai tabstop=4 shiftwidth=4 expandtab:

import logging, sys, textwrap, pprint, os, difflib, ConfigParser
import requests, json, base64, re, types, argparse, site

from cmt_client import __version__ as cmt_version
from cmt_client.exceptions import *

from types import *
from getpass import getpass

DEFAULT_CONFIG_FILE = None

# RB: config location finding logic due to stupid distutils
for config_dir_guess in [ 'etc/cmt', 'local/etc/cmt' ]:

    if os.path.exists( os.path.join( site.sys.prefix, config_dir_guess ) ):

        CONFIG_DIR = os.path.join( site.sys.prefix, config_dir_guess )
        DEFAULT_CONFIG_FILE = '%s/cmt.conf' % CONFIG_DIR
        break

def i_print( i_str, interactive ):

    if interactive:
        print i_str

def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

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

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
       parser.error("[ERROR] The file %s does not exist!"%arg)
    else:
       return open(arg,'r')  #return an open file handle

class ApiConnection:

    ENTITIES = None
    API_VERSION = None
    SESSION = None
    SSL_ROOT_CAS = None
    MANY_FIELDS = None
    AUTH_HEADER = None

    interactive = False

    def __init__( self, url=None, api_version=None, root_cas_file=None, user=None, passwd=None, interactive=False ):

        self.interactive = interactive

        self.SESSION = requests.Session()

        self.SESSION.timeout = 3.000

        self.user = user
        self.passwd = passwd

        if not url:
            #base_url = 'http://localhost:8000'
            base_url = 'https://dev.cmt.surfsara.nl'
        else:
            base_url = url

        self.set_root_ca_bundle( root_cas_file )

        if not api_version:
            self.API_VERSION = '1'
        else:
            self.API_VERSION = api_version

        self.FULL_URL = '%s/api/v%s/' %( base_url, self.API_VERSION )

        self.retrieve_entities()

    def authorization_required( self ):

        """
        Check and/or create auth header for HTTP request method
        """

        i_print('[LOGIN] Authorization required', self.interactive)

        try:
            self.AUTH_HEADER = self.create_auth_header( self.user, self.passwd )

        except CmtApiNoAuthorizationCredentials as details:

            if self.interactive:

                print '[ERROR] %s' %str(details)
                sys.exit(1)
            else:
                raise CmtApiNoAuthorizationCredentials( str(details) )

        self.SESSION.headers.update( { 'Authorization' : self.AUTH_HEADER } )

    def create_auth_header( self, user=None, passw=None ):

        """
        Create HTTP authorization header. Ask for user/passwd if run interactively
        """
        if not self.interactive:

            if not user or not passw:

                raise CmtApiNoAuthorizationCredentials('Authorization required, but no credentials supplied')

        if not user:
            user = raw_input( '[LOGIN] Username: ' )

        if not passw:
            passw = getpass( '[LOGIN] Password: ' )

        if user == '' or passw == '':

            raise CmtApiNoAuthorizationCredentials('Authorization required, but some credentials were empty!')

        base64string = base64.encodestring('%s:%s' % (user, passw)).strip()

        return "Basic %s" %base64string

    def set_content_type( self, content_type ):

        self.SESSION.headers.update( {'content-type': content_type } )

    def do_request( self, method, url, **kw_args ):

        """
        Perform some HTTP (session) request. Perform all possible error handling here
        First try unauthorized. If server says authorization is required, retry with authorization
        """

        ALLOWED_METHODS = [ 'GET', 'POST', 'UPDATE', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH' ]

        if method not in ALLOWED_METHODS:

            raise CmtApiRequestMethodNotSupported('Method %s not supported, must be one of: %s' %( method, string.join( ALLOWED_METHODS, ',' ) ) )
   
        kw_args.update( { 'verify': self.SSL_ROOT_CAS } )

        try: 
            r = self.SESSION.request( method, url, **kw_args )

        except requests.exceptions.SSLError as ssl_err:

            if not self.interactive:
                print '[ERROR] Unable to verify SSL certificate: %s' %str( ssl_err)
                print '[INFO]  Using root CAs: %s' %self.SSL_ROOT_CAS
                sys.exit(1)
            else:
                raise CmtApiSslVerificationFailed('SSL verification with root CAs %s failed: %s' %(self.SSL_ROOT_CAS, str( ssl_err)))

        except requests.exceptions.ConnectionError as req_err:

            if not self.interactive:
                print '[ERROR] Error connecting to %s: %s' %( url, str( req_ce ) )
                sys.exit(1)
            else:
                raise CmtApiConnectionError( 'Error connection to %s: %s' %( url, str( req_ce ) ) )

        if r.status_code == requests.codes.server_error:

            from tempfile import NamedTemporaryFile

            error_fp = NamedTemporaryFile( delete=False )

            error_fp.write( r.text )
            error_fp.close()

            raise CmtServerError('Contact your local CMT administrator, a server error has occured. Stored error output in: %s - please supply this file to your local CMT administrator.' %error_fp.name )

        elif r.status_code == requests.codes.unauthorized:

            # Retry request with authorization (if we have any)
            self.authorization_required()

            r = self.SESSION.request( method, url, **kw_args )

            if r.status_code == requests.codes.server_error:

                from tempfile import NamedTemporaryFile

                error_fp = NamedTemporaryFile( delete=False )

                error_fp.write( r.text )
                error_fp.close()

                raise CmtServerError('Contact your local CMT administrator, a server error has occured. Stored error output in: %s - please supply this file to your local CMT administrator.' %error_fp.name )

        #print r.status_code
        #print r.text

        if r.status_code == requests.codes.unauthorized:

            authorization_message = r.json()['detail']

            if self.interactive:

                print '[ERROR] Authorization failed: %s' %str( authorization_message )
                sys.exit(1)
            else:
                raise CmtApiAuthorizationFailed( 'Authorization failed: %s' %str( authorization_message ) )

        elif r.status_code == requests.codes.no_content:

            # HTTP 204: No content -> means request success, but no content in response (i.e. for DELETE requests)
            return True

        # This should not occur and be caught by server error handling above
        try:
            nothing = r.json()

        except ValueError as details:

            from tempfile import NamedTemporaryFile

            error_fp = NamedTemporaryFile( delete=False )

            error_fp.write( r.text )
            error_fp.close()

            if self.interactive:

                print '[ERROR] While trying to decode HTTP response as JSON: %s' %str(details)
                print '[ERROR] Stored (debug) response output in: %s - Please contact your local CMT administrator and supply this file' %error_fp.name
                sys.exit(1)
            else:
                raise TypeError( 'Error while trying to decode HTTP response as JSON: %s' %str(details) )

        return r.json()

    def retrieve_entities(self):

        kw_args = { }

        r = self.do_request( 'GET', self.FULL_URL, **kw_args )

        self.ENTITIES = r.keys()

    def set_root_ca_bundle( self, location=None ):

        default_locations = [ ]
        default_locations.append( '/etc/ssl/certs/ca-certificates.crt' ) # Debian default location
        default_locations.append( '/etc/ssl/certs/ca-bundle.crt') #Red Hat default location

        # Use location if specified
        if location:
            if os.path.exists( location ):
                self.SSL_ROOT_CAS = location
                return True
            else:
                print '[ERROR] file does not exist: %s' %location
                sys.exit(1)

        # Search for OS default locations
        for l in default_locations:

            if os.path.exists( l ):

                self.SSL_ROOT_CAS = l
                return True

        # Fallback to python module supplied CA file
        self.SSL_ROOT_CAS = requests.certs.where()
        return False

    def get_entities(self):

        if not self.ENTITIES:
            self.retrieve_entities()

        return self.ENTITIES

    def retrieve_many_fields( self, entity ):

        self.MANY_FIELDS = { }

        url = '%s/' % (self.FULL_URL + entity)

        kw_args = { }

        r = self.do_request( 'GET', url, **kw_args )

        for field_name, field_value in r['results'][0].items():

            if type( field_value ) is types.ListType:

                if not self.MANY_FIELDS.has_key( entity ):

                    self.MANY_FIELDS[ entity ] = [ ]

                if not field_name in self.MANY_FIELDS[ entity ]:

                    self.MANY_FIELDS[ entity ].append( field_name )

    def get_many_fields( self ):

        return self.MANY_FIELDS

class Client:

    API_CONNECTION = None
    interactive = False
    config_options = None

    def __init__(self, args, api_connection=None, interactive=False ):

        self.interactive = interactive

        #print '>>> Initializing client with args:', args
        self._args = None

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

        parser.add_argument('--dry-run', '-n', action='store_true', dest='dryrun', help='do a dry run')
        output_group = parser.add_mutually_exclusive_group()
        output_group.add_argument('--verbose', '-v', action='count', default=0, help='increase output verbosity')
        output_group.add_argument('--quiet', '-s', action='store_true', help='suppress output messages')
        parser.add_argument('--version', action='version', version='%(prog)s ' +str(cmt_version) )

        parser.add_argument('--config-file', '-c', type=lambda x: is_valid_file(parser,x), help='Which config file to use')

        # first parse basic options
        # need config file (settings) (if supplied) for creating API Connection..
        self.temp_args = vars(parser.parse_known_args( args )[0] )
        #print '>>> PARSED temp ARGS:', self.temp_args

        if self.temp_args.has_key( 'config_file' ):

            if type(self.temp_args[ 'config_file' ]) is not NoneType:

                self.read_config_file( self.temp_args['config_file'] )

        elif interactive:

            if os.path.exists( DEFAULT_CONFIG_FILE ):

                self.read_config_file( open( DEFAULT_CONFIG_FILE, 'r' ) )

            else:

                # currently a config file is not required.. should it be?
                pass

        if not api_connection:

            kw_args = { 'interactive': self.interactive }

            if self.config_options:
                kw_args.update( self.config_options )

            self.API_CONNECTION = ApiConnection( **kw_args )
        else:
            self.API_CONNECTION = api_connection

        ENTITIES = self.API_CONNECTION.get_entities()

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

        try:
            self._args = vars(parser.parse_args( args ))
            #print '>>> PARSED ARGS:', self._args
        except AttributeError, e:
            print '[ERROR] Invalid entity given'

    def read_config_file( self, file_object ):

        config = ConfigParser.RawConfigParser()
        config.readfp( file_object)

        self.config_options = { }

        if config.has_section( 'server' ):

            if config.has_option( 'server', 'api_version' ):
                
                self.config_options[ 'api_version' ] = config.get( 'server', 'api_version' )

            if config.has_option( 'server', 'url' ):
                
                self.config_options[ 'url' ] = config.get( 'server', 'url' )

        if config.has_section( 'ssl' ):

            if config.has_option( 'ssl', 'root_cas_file' ):
                
                self.config_options[ 'root_cas_file' ] = config.get( 'ssl', 'root_cas_file' )

        file_object.close()

    def get_args( self ):

        return self._args

    def args_to_payload(self, entity, q):
        """

        >>> args_to_payload([['cluster__name', 'cluster1'], ['rack__label', 'rack1']])
        {'rack__label': 'rack1', 'cluster__name': 'cluster1'}
        """
        d = {}

        self.API_CONNECTION.retrieve_many_fields( entity )
        MANY_FIELDS = self.API_CONNECTION.get_many_fields()

        for stmt in q:
            if MANY_FIELDS.has_key( entity ):
                if stmt[0] in MANY_FIELDS[ entity ]:
                    d[stmt[0]] = check_multiple_values( stmt[1] )
                else:
                    d[stmt[0]] = stmt[1]
            else:
                d[stmt[0]] = stmt[1]
        return d

    def create(self, args ):

        #print '>>> <CREATING>'
        # Be sure there's a --set arg before taking care of the rest of the args
        try:
            assert(args['set']), '[ERROR] Missing --set arguments'
        except AssertionError, e:

            if self.interactive:
                print e
            else:
                raise SyntaxError('Missing set arguments')

        # Prepare POST request (r) based on session (s) and given --set args
        entity = args['entity'].pop()

        self.API_CONNECTION.retrieve_many_fields( entity )

        url = '%s/' % (self.API_CONNECTION.FULL_URL + entity)
        payload = self.args_to_payload(entity, args['set'])
        #print 'PAYLOAD:', payload

        self.API_CONNECTION.set_content_type( 'application/json' )

        kw_args = { 'data' : json.dumps(payload) }

        r = self.API_CONNECTION.do_request( 'POST', url, **kw_args )

        #print '>>> </CREATING>'
        return r

    def read(self, args ):

        #print '>>> <READING>'
        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), '[ERROR] Missing --get arguments'
        except AssertionError, e:

            if self.interactive:
                print e
                return False
            else:
                raise SyntaxError('Missing get arguments')

        # Prepare GET request (r) based on session (s) and given --get args
        entity = args['entity'].pop()
        url = '%s/' % (self.API_CONNECTION.FULL_URL + entity)
        payload = self.args_to_payload(entity, args['get'])

        if args.has_key( 'fields' ):
            if args['fields'] != None:
                payload[ 'fields' ] = args['fields'][0]

        #print 'PAYLOAD:', payload

        self.API_CONNECTION.set_content_type( 'application/json' )

        kw_args = { 'params' : payload }

        r = self.API_CONNECTION.do_request( 'GET', url, **kw_args )

        #print '>>> </READING>'

        return r

    def update(self, args):

        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), '[ERROR] Missing --get arguments'
        except AssertionError, e:
            if self.interactive:
                print e
            else:
                raise SyntaxError('Missing get arguments')
            return False

        # Be sure there's a --set arg before taking care of the rest of the args
        try:
            assert(args['set']), '[ERROR] Missing --set arguments'
        except AssertionError, e:
            if self.interactive:
                print e
            else:
                raise SyntaxError('Missing set arguments')
            return False

        # Get data from given --get args to prepare a request
        entity = args['entity'].pop()
        url = '%s/' % (self.API_CONNECTION.FULL_URL + entity )
        payload = self.args_to_payload(entity, args['get'])

        self.API_CONNECTION.set_content_type( 'application/json' )

        kw_args = { 'params' : payload }

        r = self.API_CONNECTION.do_request( 'GET', url, **kw_args )

        response_data = r

        result_count = response_data[ 'count' ]

        if result_count == 0:

            if self.interactive:
                i_print('[ERROR] No objects found to update - that match: %s' %str(payload), self.interactive)
                return False
            else:
                raise CmtClientNoObjectsFound( 'No objects found to update - that match: %s' %str(payload) )

        if self.interactive:

            pprint.pprint( response_data )

            confirm_str = '[UPDATE] You are about to update: %s object(s). Are you sure ([N]/Y)?: ' %result_count
            confirm = raw_input( confirm_str )
      
            if confirm.lower() != 'y':

                return False

        self.API_CONNECTION.retrieve_many_fields( entity )

        payload = self.args_to_payload(entity, args['set'])

        update_nr = 1

        for result in response_data['results']:

            #print 'URL:', result['url']
            #print 'PAYLOAD:', payload

            i_print('[UPDATING] %s of %s ..' %( str( update_nr ), str( result_count ) ), self.interactive )

            update_nr = update_nr + 1

            kw_args = { 'data' : json.dumps(payload) }

            r = self.API_CONNECTION.do_request( 'PATCH', result['url'], **kw_args )

            #pprint.pprint( r )

        i_print('[SUCCESS] Succefully updated %s object(s)' %str(result_count), self.interactive )

    def delete(self, args):
        # Be sure there's a --get arg before taking care of the rest of the args
        try:
            assert(args['get']), '[ERROR] Missing --get arguments'
        except AssertionError, e:
            if self.interactive:
                print e
            else:
                raise SyntaxError('Missing get arguments')
            return False

        # Get data from given --get args to prepare a request
        entity = args['entity'].pop()
        url = '%s/' % (self.API_CONNECTION.FULL_URL + entity )
        payload = self.args_to_payload(entity, args['get'])
        self.API_CONNECTION.set_content_type( 'application/json' )

        kw_args = { 'params' : payload }

        r = self.API_CONNECTION.do_request( 'GET', url, **kw_args )

        response_data = r

        result_count = response_data[ 'count' ]

        if result_count == 0:

            if self.interactive:

                i_print('[ERROR] No objects found to delete - that match: %s' %str(payload), self.interactive)
                return False
            else:
                raise CmtClientNoObjectsFound( 'No objects found to delete - that match: %s' %str(payload) )

        if self.interactive:

            pprint.pprint( r )

            confirm_str = '[DELETE] You are about to delete: %s object(s). Are you sure ([N]/Y)?: ' %result_count
            confirm = raw_input( confirm_str )
      
            if confirm.lower() != 'y':

                return False

        delete_nr = 1

        for result in response_data['results']:

            #print 'URL:', result['url']

            i_print('[DELETING] %s of %s' %( str( delete_nr ), str( result_count ) ), self.interactive )

            delete_nr = delete_nr + 1

            kw_args = { }

            self.API_CONNECTION.do_request( 'DELETE', result['url'], **kw_args )

        i_print('[SUCCESS] Succefully deleted %s object(s)' %str( result_count ), self.interactive )
 
    # Parse a template
    def parse(self, args):
        #print '>>> <PARSING>'

        # Prepare POST request (r) based on session (s)
        url = self.API_CONNECTION.FULL_URL + 'template'

        payload = {}

        file_obj = args['template'][0]
        filename = file_obj.name

        files = { 'file' : file_obj }

        i_print('[SENDING] template to server and awaiting response..', self.interactive )

        kw_args = { 'params' : payload, 'files': files }

        r = self.API_CONNECTION.do_request( 'POST', url, **kw_args )

        file_obj.close()

        output_ignore_regexps = [ ]

        prompt_write = False

        if not hasattr( r, 'items' ):
            if self.interactive:
                print '[ERROR] %s' %str(response.json())
            else:
                raise RuntimeError(str(response.json()))
            return False

        if not self.interactive:
            return r

        for output_filename, output_file_attrs in r.items():

            output_file_contents = output_file_attrs['contents']
            output_file_diff_ignore = output_file_attrs['diff_ignore']

            print '[RECEIVED] output file: %s - size %d bytes' %(output_filename, len( output_file_contents ) )

            #pprint.pprint( output_file_contents )

            #pprint.pprint( output_file_diff_ignore )

            for regex in output_file_diff_ignore:

                output_ignore_regexps.append( re.compile( regex ) )

            if os.path.isfile( output_filename ):

                prompt_write = True

                print "[EXISTS] File already exists: %s" %output_filename

                if not os.access( output_filename, os.R_OK ):

                    print "[WARNING] Cannot read original file (permission denied): %s" %output_filename
                    print "[WARNING] Cannot check diff between original file and new output file"

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

                        print '[UPDATED] Received (new) output contents differs from original contents for file: %s' %output_filename
                        want_diff = raw_input( "[DIFF] Would you like to see the diff(erence)? ([N/y]): " )

                        if want_diff.lower() == 'y':

                            udiff = difflib.unified_diff( original_contents, output_list_contents, fromfile=output_filename, tofile=output_filename )

                            #udiff_list = list( udiff )

                            for uline in udiff:

                                print uline,

                            print ''

                    else:
                        print '[SAME] no difference (excluding commented lines) with original'

        if prompt_write and self.interactive:

            really_write = raw_input('[WRITE] Really write these output files? ([N/y]): ')

            if really_write.lower() != 'y':

                print "[ABORTED] Doing nothing and exiting.."
                return False

        for output_filename, output_file_attrs in r.items():

            output_file_contents = output_file_attrs['contents']

            target_dir = os.path.dirname( output_filename )

            if not os.path.isdir( target_dir ):

                if self.interactive:
                    print "[WARNING] Directory '%s' for output file '%s' does not exist" %( target_dir, output_filename )
                else:
                    raise RuntimeError("Directory '%s' does not exist" %target_dir )
                    return False

                if not os.access( target_dir, os.W_OK ):

                    if self.interactive:
                        print "[ERROR] I do not have permission to create the directory"
                        print "[ERROR] Aborting and doing nothing.."
                        return False

                want_create_dir = raw_input( "[MKDIR] You want me to create the directory? ([N/y]): " )

                if want_create_dir.lower() == 'y':

                    print "[MKDIR] creating directory: %s" %target_dir
                    os.makedirs( target_dir )

                else:

                    print "[SKIPPING] skipping output file: %s" %output_filename
                    continue

            if os.path.isfile( output_filename ) and not os.access( output_filename, os.W_OK ):

                print "[ERROR] Permission denied, file is not writeable: %s" %output_filename
                print "[SKIPPING] skipping output file: %s" %output_filename
                continue

            print "[WRITING] writing: %s " %output_filename
            f = open(output_filename, 'w')
            f.writelines(output_file_contents)
            f.close()

        print '[FINISHED] done'
        return True

def main(args):

    kw_args = { 'args' : args, 'interactive' : True }

    try:
        c = Client( **kw_args )
        parsed_args = c.get_args()
       
        # Route parsed args to the action given on command line
        command = parsed_args['func']

        if command == 'read':
            json = c.read(parsed_args)

            if json:
                pprint.pprint(json)
        elif command =='create':
            json = c.create(parsed_args)

            if json:
                pprint.pprint(json)
        elif command == 'update':
            c.update(parsed_args)
        elif command == 'delete':
            c.delete(parsed_args)
        elif command == 'parse':
            c.parse(parsed_args)

        return 0
    except SystemExit:
        return 1

if __name__ == '__main__':
    status = main(sys.argv[1:])
    print '>>> exit-status:', status
    sys.exit(status)
