#!/usr/bin/env python

#####
#
# <Setup environment for Django's DB API>
#
from sara_cmt import settings
from django.core.management import setup_environ
setup_environ(settings)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = settings.__name__
#
# </Setup environment for Django's DB API>
#
#####

#####
#
# <Some imports for our Django-template related action>
#
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
import re
#
# </Some imports for our Django-template related action>
#
#####

from types import ListType, StringTypes

import datetime

import ConfigParser
import sys

from sara_cmt.django_cli import ModelExtension, ObjectManager, QueryManager, \
    logger, parser

import sara_cmt.cluster.models


from django.db.models import get_model


def search_model(value):
    return get_model('cluster', value)


#####
#
# <Decorators/etc/cmt/>
#


def crud_validate(func):
    """
        Validate the entity given as an argument to CRUD-functions
    """

    def crudFunc(option, opt_str, value, parser, *args, **kwargs):
        model = search_model(value)
        if model:
            return func(option, opt_str, value, parser, *args, **kwargs)
        else:
            logger.error('Entity %s not known.' % (value.__repr__()))
            sys.exit(1)
    return crudFunc
#
# </Decorators>
#
#####



#####
#
# <CMT-specific settings from file>
#

# Instantiate ConfigParser
configfile = os.path.join(settings.PROJECT_BASE, '/etc/cmt/cmt.conf')
config_parser = ConfigParser.ConfigParser()
config_parser.optionxform = lambda x: x
# ^^ Hack for case-insensitivity, reference:
#    http://www.finalcog.com/python-config-parser-lower-case-names
config_parser.read(configfile)

# Setup the logger for logging
loglevel = config_parser.get('defaults', 'LOGLEVEL')
if loglevel == 'NOTSET' and settings.DEBUG == True:
    logger.setLevel(config_parser.getint('loglevels', 'DEBUG'))
else:
    logger.setLevel(config_parser.getint('loglevels', loglevel))


# Collect package information
CMTSARA_VERSION = config_parser.get('info', 'version').strip("'")
CMTSARA_DESCRIPTION = config_parser.get('info', 'description').strip("'")

#
# </CMT-specific settings from file>
#
#####



#####
#
# <Managers for database related interactions>
#
object_mgr = ObjectManager()
query_mgr = QueryManager()
#
# </Managers for database related interactions>
#
#####



#####
#
# <CRUD methods>
#


@crud_validate
def add(option, opt_str, value, parser, *args, **kwargs):
    """
        Add an object according to the given values.

        When the INTERACTIVE-flag has been set and an object is not complete
        yet, the user should be given the opportunity to add data to the
        missing fields on an interactive manner.
    """
    my_args = collect_args(option, parser)    # get method-specific args-list
    query_mgr.push_args(my_args, search_model(value), ['set'])
    query = query_mgr.get_query()

    new_obj = search_model(value)()
    logger.debug('Initiated a new %s' % new_obj.__class__.__name__)

    new_obj.setattrs_from_dict(query['set'])

    # Complete if needed (only in interactive mode)
    if parser.values.INTERACTIVE:
        new_obj.interactive_completion()

    # Save object
    save_msg = 'Added a new %s'%value
    if not parser.values.DRYRUN:
        try:
            new_obj.save()
        except Exception, e:
            logger.error('Could not add new %s: '%(value,e))
    else:
        logger.info('[DRYRUN] %s'%save_msg)


@crud_validate
def show(option, opt_str, value, parser, *args, **kwargs):
    """
        Show the objects which match the given values (queries).
    """
    # Split all given args to dict
    my_args = collect_args(option, parser)
    query_mgr.push_args(my_args, search_model(value), ['get'])
    query = query_mgr.get_query()

    objects = object_mgr.get_objects(query)

    # !!! TODO: either print short, or print long lists !!!
    # !!! TODO: use config files for fields (not) to print (maybe
    for _object in objects:
        ModelExtension.display(_object)


@crud_validate
def change(option, opt_str, value, parser, *args, **kwargs):
    """
        Search for an object which matches the given values, and change
        it/them.
    """
    my_args = collect_args(option, parser)
    query_mgr.push_args(my_args, search_model(value), ['get', 'set'])
    query = query_mgr.get_query()

    objects = object_mgr.get_objects(query)

    if objects:
        # Temporary try-except. See subtrac.sara.nl/osd/interne-services/ticket/164
        try:
            logger.info('Found %s entities matching query: %s'
                % (len(objects), ', '.join([_object.label for _object in objects])))
        except AttributeError:
            logger.info('Found %s entities matching query: %s'
                % (len(objects), ', '.join([_object.__unicode__() for _object in objects])))
        confirmed = not parser.values.INTERACTIVE or \
            raw_input('Are you sure? [Yn] ')
        if confirmed in ['', 'y', 'Y', True]:
            for _object in objects:
                attr_set_msg = 'Attributes has been set: %s' % _object
                if not parser.values.DRYRUN:
                    _object.setattrs_from_dict(query['set'])
                    logger.debug(attr_set_msg)
                else:
                    logger.debug('[DRYRUN] %s' % attr_set_msg)
        else:
            logger.info('Change has been cancelled')


@crud_validate
def remove(option, opt_str, value, parser, *args, **kwargs):
    """
        Remove the objects which match the given values (queries).
    """
    my_args = collect_args(option, parser)
    query_mgr.push_args(my_args, search_model(value), ['get'])
    query = query_mgr.get_query()

    objects = object_mgr.get_objects(query)

    if objects:
        logger.info('Found %s objects matching query: %s'\
            % (len(objects), ', '.join([_object.__str__()
                for _object in objects])))
        confirmation = not parser.values.INTERACTIVE or \
            raw_input('Are you sure? [Yn] ')
        print 'confirmation', confirmation
        # Delete and log
        if confirmation in ['', 'y', 'Y', True]:
            logger.info('deleting...')
            for _object in objects:
                del_msg = 'Deleted %s' % _object
                if not parser.values.DRYRUN:
                    _object.delete()
                    logger.info(del_msg)
                else:
                    logger.info('[DRYRUN] %s' % del_msg)

    else:
        logger.info('No existing objects found matching query')
#
# </CRUD methods>
#
#####


def generate(option, opt_str, value, parser, *args, **kwargs):
    from django.template import Context

    # Save full path of templatefile to generate
    template_filename = value

    # Make a dict with filenames of the available templates
    files = [f for f in os.listdir(settings.CMT_TEMPLATES_DIR) if f[-4:]=='.cmt']
    files.sort()

    fdict = {}
    i = 1
    for f in files:
        fdict[i] = f
        i+=1

    if template_filename[-4:] != '.cmt':
        template_filename += '.cmt'

    # Loop until a valid template has been chosen by the user
    while template_filename not in fdict.values():
        logger.warning("File '%s' not known"%template_filename)

        # Give a numbered overview of the available templates
        for key,val in fdict.items():
            print '%s : %s'%(str(key).rjust(2),val)
        logger.debug('fdict: %s'%fdict.values())
        template_filename = raw_input('\nChoose: ')

        # If number given, lookup the filename in the dictionary
        if template_filename.isdigit():
            num = int(template_filename)
            if num <= len(fdict):
                template_filename = fdict[num]
                logger.debug('filename: %s'%template_filename)
            else:
                continue
        # Else check for the extension
        elif template_filename[-4:] != '.cmt':
            template_filename += '.cmt'

        logger.debug('%s (%s)'%(template_filename,type(template_filename)))

    template_fullpath = os.path.join(settings.CMT_TEMPLATES_DIR, template_filename)

    try:
        # Initialize a Context to render the template with
        template_data = {}
        template_data['version'] = CMTSARA_VERSION
        template_data['svn_id'] = '$Id:$'
        template_data['svn_url'] = '$URL:$'
        template_data['input'] = template_fullpath
        template_data['__template_outputfiles__'] = {} # reserved for data to write to files
        context = Context(template_data)

        template_data['stores'] = template_data['__template_outputfiles__'] # to stay bw compatible with ramon's code (temporary)
        
        rendered_string = render_to_string(template_filename, context_instance=context)
        # While rendering the template there are variables added to the
        # Context, so these can be used for post-processing.
        logger.debug('<RESULT>\n%s\n</RESULT>'%rendered_string)

    except IOError, e:
        logger.error('Template does not exist: %s' % e)

    for outputfile, content in context['__template_outputfiles__'].items():
        write_msg = 'Writing outputfile: %s' % outputfile
        created_msg = 'Outputfile(s) created: %s' % outputfile

        if not parser.values.DRYRUN: # Write output file(s)
            try:
                logger.info(write_msg)
                f = open(outputfile, 'w')
                f.writelines(content)
                f.close()
                logger.info(created_msg)
            except IOError, e:
                logger.error('Failed creating outputfile: %s' % e)
            except KeyError, e:
                logger.error('No outputfiles defined in template')
        else:
            write_msg = '[DRYRUN] %s' % write_msg
            created_msg = '[DRYRUN] %s' % created_msg
            logger.info(write_msg)
            logger.info(created_msg)

    if not parser.values.DRYRUN:
        try:
            for script in context['epilogue']:
                logger.info('Executing epilogue script')
                os.system(script)
                logger.info('Finished epilogue script')
        except KeyError, e:
            logger.debug('No epilogue script found')
    return


#####
#
# <Methods for processing of arguments>
#


def collect_args(option, parser):
    """
        Collects the arguments belonging to the given option, and removes them
        from the arguments-datastructue. Returns the collected arguments as a
        list.
    """
    collected = []

    if parser.rargs:

        def floatable(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        for arg in parser.rargs:
            # stop on --foo like options
            if arg[:2] == '--' and len(arg) > 2:
                break
            # stop on -a, but not on -3 or -3.0
            if arg[:1] == '-' and len(arg) > 1 and not floatable(arg):
                break
            collected.append(arg)

        parser.largs.extend(parser.rargs[:len(collected)])
        del parser.rargs[:len(collected)]
        setattr(parser.values, option.dest, collected)

    logger.debug('Collected arguments for %s: %s' % (option, collected))
    return collected


def main():
    parser.version = CMTSARA_VERSION
    parser.description = CMTSARA_DESCRIPTION

    parser.add_option('-n', '--dry-run',
        action='store_true',
        dest='DRYRUN',
        default=config_parser.getboolean('defaults', 'DRYRUN'),
        help="""This flag has to be given before -[aclmr]""")
    parser.add_option('--script',
        action='store_false',
        dest='INTERACTIVE',
        default=config_parser.getboolean('defaults', 'INTERACTIVE'))
    parser.add_option('-a', '--add',
        action='callback',
        callback=add,
        type='string',
        metavar='ENTITY',
        nargs=1,
        help="""Add an object of given ENTITY.

            arguments:   set <ASSIGNMENTS>

            The object will get values according to the given assignments. 
            Assignments could be formed like [<FK>__]<attr>=<value>""")
    parser.add_option('-c', '--change',
        action='callback',
        callback=change,
        type='string',
        metavar='ENTITY',
        nargs=1,
        help="""Change value(s) of object(s) of given ENTITY.

            arguments:   get <QUERY> set <ASSIGNMENTS>

            The query, which consists out of one or more terms, is used to make
            a selection of objects to change. These objects will be changed
            according to the given assignments.""")
    parser.add_option('-g', '--generate',
        action='callback',
        callback=generate,
        type='string',
        metavar='TEMPLATE',
        nargs=1,
        help='Render the given template')
    parser.add_option('-l', '--list',
        action='callback',
        callback=show,
        type='string',
        metavar='ENTITY [ATTRIBUTE=VALUE]',
        nargs=1,
        help="""List object(s) of the given ENTITY.

            arguments:   get <QUERY>

            The query, which consists out of one or more terms, is used to make
            a selection of objects to list.""")
    parser.add_option('-r', '--remove',
        action='callback',
        callback=remove,
        type='string',
        metavar='ENTITY [ATTRIBUTE=VALUE]',
        nargs=1,
        help='Remove objects which reflect the given query')

    # TODO: implement the following option(s)
    parser.add_option('-v', '--verbose',
        action='store_true',
        dest='VERBOSE',
        default=config_parser.getboolean('defaults', 'VERBOSE'))

    (options, args) = parser.parse_args()
    logger.debug('(options, args) = (%s, %s)' % (options, args))

    if len(sys.argv) == 1:
        # No arguments are given
        parser.print_help()
        return 1

    return 0
#
# </Methods for processing of arguments>
#
#####


if __name__ == '__main__':
    status = main()
    sys.exit(status)
