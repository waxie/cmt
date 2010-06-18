#!/usr/bin/python

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
from sara_cmt.parser import Parser

import sara_cmt.cluster.models


from django.db.models import get_model


def search_model(value):
    return get_model('cluster', value)


#####
#
# <Decorators>
#


def crud_validate(func):
    """
        Validate the entity given as an argument to CRUD-functions
    """

    def crudFunc(option, opt_str, value, parser, *args, **kwargs):
        model = search_model(value)
        if model != None:
            logger.debug("Assuming '%s' should be of type %s"
                % (value, model._meta.object_name))
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
configfile = os.path.join(os.path.dirname(__file__), 'cmt.cfg')
config_parser = ConfigParser.ConfigParser()
config_parser.optionxform = lambda x: x
# ^^ Hack for case-insensitivity, reference:
#    http://www.finalcog.com/python-config-parser-lower-case-names
config_parser.read(configfile)

# Setup the logger for logging
loglevel_str = config_parser.get('defaults', 'LOGLEVEL')
logger.setLevel(config_parser.getint('loglevels', loglevel_str))


# Collect package information
CMTSARA_VERSION = config_parser.get('info', 'version').strip("'")
CMTSARA_DESCRIPTION = config_parser.get('info', 'description').strip("'")

parse_object = Parser()
parser = parse_object.getParser()

# Get and set the defaults
DRYRUN = config_parser.getboolean('defaults', 'DRYRUN')
INTERACTIVE = config_parser.getboolean('defaults', 'DRYRUN')
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

    if parser.values.INTERACTIVE:
        new_obj.interactive_completion()


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
    for object in objects:
        ModelExtension.display(object)


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
        logger.debug('Found %s entities matching query: %s'
            % (len(objects), objects))
        confirmed = not parser.values.INTERACTIVE or \
            raw_input('Are you sure? [Yn] ')
        if confirmed in ['', 'y', 'Y', True]:
            for object in objects:
                if not parser.values.DRYRUN:
                    object.setattrs_from_dict(query['set'])
                    logger.debug('Attributes has been set: %s' % object)
                else:
                    logger.debug('[DRYRUN] Attributes has been set: %s'
                        % object)
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
            % (len(objects), ', '.join([object.__str__()
                for object in objects])))
        confirmation = not parser.values.INTERACTIVE or \
            raw_input('Are you sure? [Yn] ')
        print 'confirmation', confirmation
        # Delete and log
        if confirmation in ['', 'y', 'Y', True]:
            logger.info('deleting...')
            for object in objects:
                if not parser.values.DRYRUN:
                    object.delete()
                    logger.info('Deleted %s' % object)
                else:
                    logger.info('[DRYRUN] Deleted %s' % object)

    else:
        logger.info('No existing objects found matching query')
#
# </CRUD methods>
#
#####


def generate(option, opt_str, value, parser, *args, **kwargs):
    from sara_cmt.template import CMTTemplate
    from django.template import Context
    # !!! TODO: Do this in the templates
    from sara_cmt.cluster.models import Cluster, HardwareUnit, Interface, Network # for template_data

    # Save full path of templatefile to generate
    filename = '%s.cmt' % value
    fullpath = os.path.join(settings.CMT_TEMPLATES_DIR, '%s.cmt' % value)

    # Load the contents of the templatefile as a CMTTemplate
    try:
        f = open(fullpath, 'r')
        templatestr = f.read()
        f.close()

        ### <DEBUG>
        #logger.debug('<TEMPSTR>\n%s'%templatestr)
        #logger.debug('</TEMPSTR>')
        ### </DEBUG>

        template = CMTTemplate(templatestr)

        # Render the CMTTemplate with a Context
        template_data = {}
        template_data['version'] = CMTSARA_VERSION
        template_data['svn_id'] = '$Id:$'
        template_data['svn_url'] = '$URL:$'
        template_data['input'] = fullpath
        # !!! TODO: Change from hardcoded to dynamic:
        template_data['Cluster'] = Cluster
        template_data['HardwareUnit'] = HardwareUnit
        template_data['Interface'] = Interface
        template_data['Network'] = Network

        c = Context(template_data)
        res = template.render(c)

        # While rendering the CMTTemplate there are variables added to the
        # context, so these can be used for post-processing.

        ### <DEBUG>
        #logger.debug('<CONTEXT>\n%s'%c)
        #logger.debug('</CONTEXT>')
        logger.debug('<RESULT>\n%s'%res)
        logger.debug('</RESULT>')
        ### </DEBUG>
    except IOError, e:
        logger.error('Template does not exist: %s' % e)

    ### <DEBUG>
    #logger.info('Now executing epilogue script')
    #logger.debug('<EPILOGUE>')
    #os.system(c['epilogue'])
    #logger.debug('</EPILOGUE>')
    #logger.info('Finished epilogue script')
    ### </DEBUG>

    try:
        logger.info('Writing outputfile')
        f = open(c['output'], 'w')
        f.writelines(res)
        f.close()
        logger.info('Outputfile is created')
    except IOError, e:
        logger.error('Failed creating outputfile: %s' % e)
    except KeyError, e:
        logger.error('No output defined in template')
    return


def mac(option, opt_str, value, parser, *args, **kwargs):
    """
        Change the MAC-address of an existing interface.
    """
    old_mac, new_mac = value

    query = {'ent': search_model('interface'),
        'get': {'hwaddress': [old_mac]}, 'set': {'hwaddress': [new_mac]}}

    object = object_mgr.get_object(query)

    if object:
        logger.debug('Found a unique object matching query: %s' % object)
        confirmed = not parser.values.INTERACTIVE or \
            raw_input('Are you sure? [Yn] ')
        if confirmed in ['', 'y', 'Y', True]:
            if not parser.values.DRYRUN:
                object.setattrs_from_dict(query['set'])
                logger.debug('Attributes has been set: %s' % object)
            else:
                logger.debug('[DRYRUN] Attributes has been set: %s' % object)
        else:
            logger.info('Change of MAC-address has been cancelled')
    else:
        logger.error('Unable to execute this request')
#
# </Database related methods>
#
#####


#####
#
# <Methods for processing of arguments>
#
#def collect_args(option):


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
                    default=config_parser.getboolean('defaults',
                                                     'INTERACTIVE'))
    parser.add_option('-a', '--add',
                    action='callback',
                    callback=add,
                    type='string',
                    metavar='ENTITY',
                    nargs=1,
                    help="""Add an object of given ENTITY.

                        arguments:   set <ASSIGNMENTS>

                        The object will get values according to the given
                        assignments. Assignments could be formed like
                        [<FK>__]<attr>=<value>""")
    parser.add_option('-c', '--change',
                    action='callback',
                    callback=change,
                    type='string',
                    metavar='ENTITY',
                    nargs=1,
                    help="""Change value(s) of object(s) of given ENTITY.

                        arguments:   get <QUERY> set <ASSIGNMENTS>

                        The query, which consists out of one or more terms, is
                        used to make a selection of objects to change. These
                        objects will be changed according to the given
                        assignments.""")
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

                        The query, which consists out of one or more terms, is
                        used to make a selection of objects to list.""")
    parser.add_option('-m', '--mac',
                    action='callback',
                    callback=mac,
                    type='string',
                    metavar='<old MAC> <new MAC>',
                    nargs=2,
                    help='Change the MAC-address of an interface')
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
                    dest='verbose',
                    default=False)

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
