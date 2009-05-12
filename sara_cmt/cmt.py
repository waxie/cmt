#!/usr/bin/python

#####
#
# <Setup environment for Django's DB API>
#
from django.template.loader import render_to_string # to generate templates
from sara_cmt import settings
from django.core.management import setup_environ
setup_environ(settings)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = settings.__name__
#
# </Setup environment for Django's DB API>
#
#####

from types import ListType, StringTypes

import datetime

import optparse
import ConfigParser
import sys



import sara_cmt.cluster.admin
from sara_cmt.django_cli import ModelExtension
from sara_cmt.logger import Logger


import sara_cmt.cluster.models



#####
#
# <CMT-specific settings from file>
#

# Instantiate ConfigParser
configfile = os.path.join(os.path.dirname(__file__),'cmt.cfg')
config_parser = ConfigParser.ConfigParser()
config_parser.optionxform = lambda x: x
# ^^ Hack for case-insensitivity, reference:
#    http://www.finalcog.com/python-config-parser-lower-case-names
config_parser.read(configfile)

# Get global logger
logger = Logger().getLogger()
loglevel_str = config_parser.get('defaults','LOGLEVEL')
logger.setLevel(config_parser.getint('loglevels',loglevel_str))

# Collect package information
CMTSARA_VERSION = config_parser.get('info','version').strip("'")
CMTSARA_DESCRIPTION = config_parser.get('info','description').strip("'")

# Make a dict with aliasses for the models
entities = {}
for option in config_parser.options('entities'):
  labels = config_parser.get('entities',option).split(',')
  for label in labels:
    entities[label] = sara_cmt.cluster.models.__getattribute__(option)

# Get and set the defaults
DRYRUN = config_parser.getboolean('defaults','DRYRUN')
INTERACTIVE = config_parser.getboolean('defaults','DRYRUN')
#
# </CMT-specific settings from file>
#
#####


#####
#
# <Database related methods>
#
def add(option, opt_str, value, parser, *args, **kwargs):
  """
    Add an object according to the given values.
    
    When the INTERACTIVE-flag has been set and an object is not complete yet,
    the user should be given the opportunity to add data to the missing fields
    on an interactive manner.
  """
  # First be sure a valid entity has been given
  try:
    new_object = entities[value]()
  except KeyError:
    logger.error('%s is not a valid entity' % value.__repr__())
    sys.exit(1)
    
  # Assign values to attributes if assignments are given.
  queries = collect_args(option, parser)
  queries_dict = queries_to_dict(queries)
  new_object.setattrs_from_dict(queries_dict)
    
  # Let the user complete interactively if INTERACTIVE-flag has been set.
  if parser.values.INTERACTIVE:
    new_object.interactive_completion()

  # ??? TODO: Validate object ???

  # Save and log
  if not parser.values.DRYRUN:
    try:
      new_object.save()
      logger.info('Saved %s with id %s' % (new_object._meta.verbose_name, new_object.pk))
    except (ValueError, sqlite3.IntegrityError), e:
      logger.error('Failed to save %s: %s' % (new_object._meta.verbose_name, e))
  else:
    logger.info('Normally the %s should be saved now' % new_object._meta.verbose_name)
    logger.debug('%s: %s' % (entities[value], new_object.__dict__))



def remove(option, opt_str, value, parser, *args, **kwargs):
  """
    Remove the objects which match the given values (queries).
  """
  # First search existing objects which match the given queries.
  queries_dict = queries_to_dict(parser.rargs) # ??? TODO: tuple-list instead of dict ???
  logger.debug(queries_dict)
  objects_qset = ModelExtension._queries_to_qset(entities[value], queries_dict)

  if objects_qset:
    logger.info('Found %s objects matching query: %s'\
      % (len(objects_qset), ', '.join([object.__str__() for object in objects_qset])))
    confirmation = not parser.values.INTERACTIVE or raw_input('Are you sure? [Yn] ')
    print 'confirmation', confirmation
    # Delete and log
    if confirmation in ['', 'y', 'Y', True]:
      logger.info('deleting...')
      for object in objects_qset:
        if not parser.values.DRYRUN:
          object.delete()
          logger.info('Deleted %s' % object)
        else:
          logger.info('Normally the %s should be deleted now' % object._meta.verbose_name)
          
  else:
    logger.info('No existing objects found matching query')




def _search(entity_type, queries):
  """
    Search for entities which match the given query.
    Returns a queryset.
  """
  
  # TODO: !!! Delegate this task to a function in the ModelExtension !!!

  return NotImplementedError
#  try:
#    assert queries, "Maybe you'll get better results with a query/filter."
#  except AssertionError, err:
#    logger.info(err)
#    
#  arg_dict = queries_to_dict(queries)
#
#  if queries in [[],['all']]: # ??? Maybe only ['all'] to use [] for interactive query ???
#    entities_qset = entities[entity_type].objects.all()
#  else:
#    # Make a QuerySet based on the given query, and return it
#    entities_qset = entities[entity_type].objects.complex_filter(arg_dict)
#  logger.debug('Found %s entities reflecting the following args: %s'\
#    % (len(entities_qset), queries))
#  return entities_qset



def change(option, opt_str, value, parser, *args, **kwargs):
  """
    Search for an object which matches the given values, and change it/them.
  """
  # TODO: Implement for usage like `cmtsara --change <entity> <query> <assignments>
  #
  # queries => dict of tuples
  #
  # --change <entity> <query> <assignments>
  #
  # should become something like:
  #
  # {query:<set of queries>, assignments:<set of assignments>}
  entities_found = _search(value[0], value[1])

  if entities_found:
    print 'Found %s entities matching query: %s'\
      % (len(entities_found), ', '.join([entity.__str__() for entity in entities_found]))
    # TODO: !!! Make multiple changes possible in value[2]
    field, change = value[2].split('=')
    confirmed = not parser.values.INTERACTIVE or raw_input('Are you sure? [Yn] ')
    if confirmed in ['', 'y', 'Y', True]:
      print 'changing...'
      for entity in entities_found:
        if not parser.values.DRYRUN:
          print 'before :', entity.__dict__
          entity._setattr(field, change)
          entity.save()
          print 'after  :', entity.__dict__
        print 'changed', entity._meta.verbose_name, entity
  else:
    print 'No entities found matching query'




def show(option, opt_str, value, parser, *args, **kwargs):
  queries = queries_to_dict(parser.rargs) # ??? tuple-set instead of dict ???
  logger.debug(queries)
  entities_found = ModelExtension._queries_to_qset(entities[value], queries)

  # !!! TODO: either print short, or print long lists !!!
  for entity in entities_found:
    ModelExtension.display(entity)




def generate(option, opt_str, value, parser, *args, **kwargs):
  # Put data in a dictionary to make accessible in the templates
  template_data = {}
  for entity in entities.values():
    template_data[entity._meta.object_name] = entity
  template_data['version'] = CMTSARA_VERSION
  template_data['svn_id'] = '$Id:$'
  template_data['svn_url'] = '$URL:$'

  try:
    # Render a string of the template from the argument
    template_string = render_to_string('ported/'+value+'.cmt', template_data)

    # Remove blanks from the output of Django Template Engine
    whitespace = r'\n(\s*\n)*'
    lines = re.sub(whitespace, '\n', template_string).splitlines()
    parsed_str = '\n'.join([line for line in lines if line])

    # Insert blank lines where they are needed
    cleaned_data = parsed_str.replace('{ BLANKLINE }\n', '\n')

    # !!! TODO: save the generated file !!!
    # !!! TODO: execute command to reload the generated file !!!
    print cleaned_data
  except TemplateDoesNotExist, e:
    print TemplateDoesNotExist, e

  return



def mac(option, opt_str, value, parser, *args, **kwargs):
  """
    Change the MAC-address of an existing interface.
  """
  old_mac, new_mac = value[0], value[1]
  try:
    interface = Interface.objects.get(mac=old_mac)
    interface.mac = new_mac
    interface.save()
    logger.info('MAC-address of interface %s has been changed from %s to %s' %
      (interface.name, old_mac, new_mac))
  except Interface.DoesNotExist, e:
    logger.error('%s %s' % (Interface.DoesNotExist, e))

#
# </Database related methods>
#
#####


#####
#
# <Methods for processing of arguments>
#
def queries_to_dict(queries):
  """
    Build a dictionary from the args given to the optionparser. Args can be
    given as a string or an array of strings. For example:
    
    both 'id=2,hostname=node1,rack=3' and ['id=2', 'hostname=node1', 'rack=3']
    
    should be translated to:
    
    {'hostname':'node1', 'rack':'3', 'id':'2'}

    When a single option is given multiple times, the value should be a list.
    For example:

    'hostname=node1,rack=3,rack=4' or ['hostname=node1', 'rack=3', 'rack=4']

    should become
    
    {'hostname':'node1', 'rack':['3', '4']}
  """
  _q = queries
  # First be sure to have a list with queries
  if isinstance(queries, StringTypes):
    queries = [queries]
  
  # Now convert the list of single queries to a dictionary, with attributes as
  # keys and corresponding values as values. So the result will be something
  # like {('<attr>':'<val>')+}.

  result = {}
  for query in queries:
    query = query.split(',')
    for q in query:
      (opt,val) = q.split('=')
      if result.has_key(opt):
        if isinstance(result[opt], ListType):
          # This option has been parsed multiple times
          result[opt].append(val)
        else:
          # This option has been parsed one time
          result[opt] = [result[opt],val]
      else:
        # Parsing this option for the very first time
        result[opt] = val

  logger.debug('queries_to_dict(%s) => %s' % (_q, result))
  return result


def queries_to_lists(queries):
  """
    Returns a list of lists. Those lists are based on the the items from the
    output of queries_to_dict(queries). For example:

    'hostname=node1,rack=3,rack=4' or ['hostname=node1', 'rack=3', 'rack=4']

    should become
    
    [['hostname', 'node1'], ['rack', ['3', '4']]]
  """
  result = [list(item) for item in queries_to_dict(queries).items()]
  logger.debug('queries_to_lists(%s) => %s' % (queries, result))
  return result


def queries_to_tuples(queries):
  """
    Returns a list of tuples. Those tuples are based on the the items from the
    output of queries_to_dict(queries). For example:

    'hostname=node1,rack=3,rack=4' or ['hostname=node1', 'rack=3', 'rack=4']

    should become
    
    [('hostname', 'node1'), ('rack', ['3', '4'])]
  """
  result = queries_to_dict(queries).items()
  logger.debug('queries_to_tuples(%s) => %s' % (queries, result))
  return result


def collect_args(option, parser):
  """
    Collects the arguments belonging to the given option, and removes them from
    the arguments-datastructue.
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

  return collected



def main():
  # ??? TODO: parser options for '--query' and '--assign'
  #           or maybe '--get' and '--set'
  # ???
  parser = optparse.OptionParser(version=CMTSARA_VERSION,
                                 description=CMTSARA_DESCRIPTION)

  parser.add_option('-n', '--dry-run',
                    action='store_true',
                    dest='DRYRUN',
                    default=config_parser.getboolean('defaults','DRYRUN'))
  parser.add_option('--script',
                    action='store_false',
                    dest='INTERACTIVE',
                    default=config_parser.getboolean('defaults','INTERACTIVE'))
  parser.add_option('-a', '--add',
                    action='callback',
                    callback=add,
                    type='string',
                    metavar='ENTITY',
                    nargs=1,
                    help='Add an object of type ENTITY, with optionally ' + \
                      'attributes set like assignments given in the form ' + \
                      'of <attr>=<value> or <FK>__<attr>=<value>.')
  parser.add_option('-c', '--change',
                    action='callback',
                    callback=change,
                    type='string',
                    metavar='ENTITY [ATTRIBUTE=VALUE] [ATTRIBUTE=VALUE]',
                    nargs=3,
                    help='Change the value of an object.')
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
                    help='List objects that appear to reflect the given attributes')

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
  

  (options, args) = parser.parse_args()

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
