from django.db.models.fields import FieldDoesNotExist 
from django.db.models.fields.related import ForeignKey, ManyToManyField

from types import StringTypes

import sqlite3
from sqlite3 import IntegrityError

from sara_cmt.logger import Logger
logger = Logger().getLogger()

import sara_cmt
from django.db import models
CLUSTER_MODELS = 'sara_cmt.cluster.models'

import tagging
from tagging.fields import TagField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

class ModelExtension(models.Model):
  """
    The ModelExtension of Django-CLI is meant as a Mixin for a Django Model.
  """
  tags       = TagField()
  created_on = CreationDateTimeField()
  updated_on = ModificationDateTimeField()
  note       = models.TextField(blank=True)


  class Meta:
    abstract = True


#####
#
# <STATIC METHODS>
#
  @staticmethod
  def _required_fields(model):
    """
      Checks which fields of the given model are required.
      Returns the set of required fields.
    """
    required = [field for field in model._meta.fields if not field.blank]
    return required


  @staticmethod
  def _required_fields_no_fks(model):
    """
      Returns the result of _required_fields without FKs.
    """
    required = [field for field in ModelExtension._required_fields(model)
      if not isinstance(field, ForeignKey)]
    return required


  @staticmethod
  def _required_fields_fks_only(model):
    """
      Returns FKs from the result of _required_fields.
    """
    required = [field for field in ModelExtension._required_fields(model)
      if isinstance(field, ForeignKey)]
    return required


  @staticmethod
  def _is_fk(model, field):
    """
      Look if a field is defined as a ForeignKey. Returns a boolean.
    """
    if isinstance(field, StringTypes):
      field = model._meta.get_field(field)
    return isinstance(field, ForeignKey)


  ####
  # TODO: <Move to QueryManager>
  #
  @staticmethod
  def _values(model, fields=None):
    """
      This function is like the QuerySet.values() in Django. Difference is that
      the query of _values will be restricted to the required fields in the
      given model, minus 'id' and FKs. When a fields-argument is given, only
      the values of that field(s) will be returned.
      Returns a ValuesQuerySet (like Django's QuerySet.values() does).
    """
    if fields:
      wanted_fields = ','.join([field.__repr__() for field in fields])
    else:
      # If no fields are given, just filter on all required fields (except FKs)
      wanted_fields = ','.join([field.name.__repr__()
        for field in ModelExtension._required_fields_no_fks(model)])
    wrapper_cmd = "%s.%s.objects.values('id',%s)" % (CLUSTER_MODELS, model.__name__, wanted_fields)
    logger.debug('Built command: %s' % wrapper_cmd)
    vqset = eval(wrapper_cmd)
    return vqset


  @staticmethod
  def search_object_ids(model, value, fields=None):
    """
      Search for objects of the given model. This method will find objects with
      the given value in the (list of) given field(s).
      Returns a list of matching object-ids.
    """
    matching_indices = []
    # Only search in the required fields of the model
    search_space = ModelExtension._values(model, fields)
    #logger.debug('Search space: %s' % search_space)
    
    # Search for objects containing the given value...
    for entity in search_space:
      for (key,val) in entity.items():
        # ... but only search for matches in the non-id-fields
        if val.__str__() == value and key is not 'id':
          matching_indices.append(entity['id'])
          break
    return matching_indices
  #
  # </Move to QueryManager>
  ####

  @staticmethod
  def display(instance):
    """
      Print all values given in list_display of the model's admin
    """
    # First get access to the admin
    admin_class_name = instance._meta.object_name+'Admin'
    admin_list_display = eval('sara_cmt.cluster.admin.'+admin_class_name+'.list_display')

    # Determine longest value-string to display
    longest_key = 0
    for val in admin_list_display:
      if len(val) > longest_key:
        longest_key = len(val)

    # Print the values
    print ' .---[  %s  ]---' % instance
    for key in admin_list_display:
      if key not in ('__unicode__','__str__'):
        print ' : %s : %s' % (key.ljust(longest_key),instance.__getattribute__(key))
    print " '---\n"
#
# </STATIC METHODS>
#
#####


  def is_complete(self):
    """
      Check if all the required fields has been assigned.
    """
    return not self._missing_fields()

    
  def setattrs_from_dict(self, arg_dict):
    """
      Set attributes according to the arguments, given in a dictionary. Each
      key in the dictionary should match an attribute name in the model. Checks
      are delegated to the _setattr-function.
    """
    for arg in arg_dict:
      logger.debug('checking arg: %s(%s)'%(arg,arg_dict[arg]))

      # In case of an id-field: Just ignore it.
      if arg == 'id':
        logger.debug('Skipping arg with id-field')
        continue

      #fieldtype = 
      elif arg.find('__') is -1:
        # Then assume it's a regular field.
        # !!! TODO: First make sure it's a regular field. !!!
        logger.debug('Trying to set a regular field')
        self._setattr(field=arg, value=arg_dict[arg])
        continue
      else:
        # Probably it's a FK field; This one needs a special treatment. Args
        # like 'rack__label' should be split up to ['rack', '__', 'label']. Or
        # more generic: '<FK>__<attr>' should become ['<FK>', '__', '<attr>'].
        # !!! TODO: First make sure it's a regular field. !!!
        partitioned = arg.partition('__')
        fk, attr = partitioned[0], partitioned[2]
        fld = self._meta.get_field(fk)
        val = arg_dict[arg]
        # Multiple subfields can be concatenated with '+'-chars when given via
        # args. If an argument like '<FK>__<attr1>+<attr2>' is given, CMTSARA
        # should filter on the fields <attr1> and <attr2> in the model which
        # belongs to the FK.
        subs = attr.split('+')
        logger.debug("Trying to set FK '%s' to id of match for '%s in field(s) %s'" % (fld.name,val,subs))
        logger.debug('partitioned: %s' % ', '.join([part.__repr__() for part in partitioned]))

        self._setfk(field=fld, subfields=subs, value=val)
        continue

    logger.debug('attrs_from_dict(%s) => %s' % (arg_dict,self.__dict__))
    

  def _missing_fields(self):
    """
      Checks if the required fields all have a value assigned to it, to be sure
      it can be saved to the database.
      Returns the set of missing editable fields.
    """
    required, missing = ModelExtension._required_fields(self.__class__), []

    # Isolate all missing fields from required fields.
    for field in required:
      try:
        if not self.__getattribute__(field.name) and field.editable: # Field hasn't been set
          missing.append(field)
      except: # FK hasn't been set
        missing.append(field)
    return missing


  def interactive_completion(self):
    """
      Lets the user assign values to the missing fields, by iterating over the
      missing fields. Iteration will stop when all required fields are given.
    """
    # !!! Note: This function should only be called in INTERACTIVE mode. !!!
    # ??? TODO: Check raw_input for ValueError. ???
    
    # !!! TODO: Validation via forms:
    #           http://docs.djangoproject.com/en/dev/ref/forms/validation/ !!!

    missing = self._missing_fields()

    while missing:
      logger.info('Missing required attributes: %s'
        % ' '.join([field.name for field in missing]))

      current_field = missing[0]
      input = raw_input(current_field.verbose_name+': ')
      try:
        assert bool(input), 'Field cannot be left blank'
        # Input for missing attribute is now stored in variable 'input'.
        #i = self._setattr(current_field, input)
        #self.save()
        self._setattr(current_field, input)
        missing.remove(current_field)
      except AssertionError, err:
        logger.error(err)
      except sqlite3.IntegrityError, err:
        logger.error('IntegrityError:', err)

      logger.debug('Current values: %s' % self.__dict__)
      missing = self._missing_fields()



  def _setfk(self, field, value, subfields=None):
    """
      Set the FK of the given field to the id of an object with the given value
      in one of its required fields (minus 'id' and FKs).
    """
    logger.debug('(field,value): (%s,%s)'%(field,value))
    to_model = field.rel.to
    logger.debug('FK to %s'%to_model.__name__)

    # determine which fields should be searched for
    if not subfields:
      subfields = to_model._required_fields(to_model)
      logger.debug('Filter is set to required fields of %s: %s'%(to_model.__name__,[field.name for field in subfields]))

    # make kwargs dict
    kwargs = {}

    for subfield in subfields:
      kwargs['%s__icontains'%subfield.name] = value

    logger.debug('kwargs: %s'%kwargs)

    # filter
    objects = to_model.objects.filter(**kwargs)
    object_count = len(objects)
    if object_count is 0:
      logger.warning('No matching object found; Change your query.')
      pass
    elif object_count is 1:
      logger.debug('Found 1 match: %s'%objects)
      object = objects[0]
      #object = objects.latest('id')
      logger.debug('object: %s'%object)
      logger.debug('field.attname: %s'%field.attname)
      logger.debug('field.name: %s'%field.name)
      self.__setattr__(field.attname, object.id)
      logger.info('%s now references to %s'%(field.name,object))
    else:
      # !!! TODO: let the user refine the search !!!
      logger.info('To many matching objects; Refine your query.')
      pass



  def _setm2m(self, field, value, subfield=None):
    """
      Set a ManyToMany-relation.
    """
    pass
      


  def _setattr(self, field, value):
    """
      Assign the given value to the attribute belonging to the given field. The
      field can be given as a field in the model, or as the string matching its
      name.
      When given as a string, it may be followed by '__<attr>', to search for
      already existing entities with the <attr>-field equal to the given value.
      If the search results to a single match, the id of the matching entity is
      assigned to the given ForeignKey-field.
    """
    # First init the field itself if it's given as a string
    if isinstance(field, StringTypes):
      field = self._meta.get_field(field)

    # !!! TODO: Quick {che,ha}ck; have to check this once more !!!
    if isinstance(value, list):
      value = value[0]

    logger.debug('field=%s (%s), value=%s' % (field.name,field.__class__.__name__,value.__repr__()))

    assert isinstance(value, StringTypes), "Given value is a %s, which isn't supported yet (still have to implement this)" % type(value) # !!! TODO: implement support for lists of values !!!
    if isinstance(field, ForeignKey):
      logger.debug('I am a %s'%type(self))
      logger.debug('FK to %s'%field.rel.to)
      logger.debug('(field,value): (%s,%s)'%(field,value))
      self._setfk(field, value)
    elif isinstance(field, ManyToManyField):
      logger.debug('We found a M2M field, but first have to implement a function to handle this')
      pass
      # !!! TODO: Implement M2M relations !!!
    else:
      logger.debug('We have to handle a %s'%type(field))
      self.__setattr__(field.name, value)

    if self.is_complete():
      try:
        if parser.values.DRYRUN:
          self.save() # !!! TODO: disable at dry-runs
          logger.info('Saved %s'%self)
        else:
          logger.info('[DRYRUN] Saved %s'%self)
      except (sqlite3.IntegrityError, ValueError), err:
        logger.error(err)



class ObjectManager():
  def __init__(self):
    logger.info('Initialized an ObjectManager')

  def get_objects(self, query):
    """
      Retrieve objects from the database, corresponding to the entity and terms
      in the given query. The terms are OR-ed by default.
    """
    # !!! TODO: Implement AND !!!
    kwargs = {}
    
    for attr, val in query['get'].items():
      try:
        fld = query['ent']._meta.get_field(attr)
        # Default field to search in
        if fld.rel.to().__dict__.has_key('label'):
          label = 'label'
        else:
          label = 'name'
        if type(fld) == ForeignKey:
          attr = '%s__%s'%(attr,label) # ??? TODO: maybe use %s__str ???
          # FK-specific code...
        elif type(fld) == ManyToManyField:
          attr = '%s__%s'%(attr,label) # ??? TODO: maybe use %s__str ???
          # M2M-specific code...
        kwargs['%s__in'%attr] = val
      except FieldDoesNotExist, err:
        logger.error(err)

    objects = query['ent'].objects.filter(**kwargs)
    return objects


    
class QueryManager():

  def __init__(self):
    logger.info('Initialized QueryManager')
    self.query = self.Query()

  class Query(dict):
    """
      Query holds a dictionary of the given args.
    """
    def __init__(self):
      self._new()

    def _new(self):
      self['ent'] = None
      self['get'] = {}
      self['set'] = {}
      logger.info('Built new Query: %s'%self)

    def as_tuple(self):
      """
        Returns a tuple of tuples. Those tuples are based on the the items from
        the output of queries_to_dict(queries). For example:

        {'hostname':'node1', 'rack':['3', '4']}

        should become

        (('hostname', 'node1'), ('rack', ('3', '4')))
      """
      # TODO: implement function which converts a (nested) dict into a (nested) tuple
      pass

    def as_list(self):
      """
        Returns a list of lists. Those lists are based on the the items from the
        output of queries_to_dict(queries). For example:

        {'hostname':'node1', 'rack':['3', '4']}

        should become

        [['hostname', 'node1'], ['rack', ['3', '4']]]
      """
      # TODO: implement function which converts a (nested) dict into a (nested) list
      pass


  def translate(self, given_queries):
    """
      Translate the given user input to a Query-object. The user input should
      be given as a dictionary which looks like:
        {'ent':<entity_type>, 'get':<arg_list>, 'set':<arg_list>}
    """
    # ??? TODO: first cleanup the query? ???
    
    # Save the entity type in the query
    self.query['ent'] = given_queries.pop('ent')

    # Save the get- and set-subqueries in the query
    for key, given_subqueries in given_queries.items():
      if given_subqueries is not None:
        # Convert the list of single arguments to dictionary-items, so:
        #   ['attr1=val1', 'attr2=val2']
        # will become
        #   {'attr1': 'val1', 'attr2': 'val2'}
        for arg in given_subqueries:
          (k,val) = arg.split('=',1)

          # ??? split the val in case of ranges ???
          
          if self.query[key].has_key(k):
            self.query[key][k].append(val)
          else:
            self.query[key][k] = [val]

    logger.debug("translated args %s into dict %s"%(given_queries,self.query))
    return self.query

  def get_query(self):
    return self.query
