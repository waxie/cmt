from django.db.models.fields.related import ForeignKey

from types import StringTypes

import sqlite3
from sqlite3 import IntegrityError

from sara_cmt.logger import Logger
logger = Logger().getLogger()

import sara_cmt
from django.db import models
CLUSTER_MODELS = 'sara_cmt.cluster.models'

class ModelExtension():
  """
    The ModelExtension of Django-CLI is meant as a Mixin for a Django Model.
  """

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
      if not isinstance(field, ForeignKey)]
    return required


  @staticmethod
  def _is_complete(model):
    """
      Check if all the required fields has been assigned.
    """
    return not ModelExtension._missing_fields(model)


  @staticmethod
  def _is_fk(model, field):
    """
      Look if a field is defined as a ForeignKey. Returns a boolean.
    """
    if isinstance(field, StringTypes):
      field = model._meta.get_field(field)
    return isinstance(field, ForeignKey)

  @staticmethod
  def _queries_to_qset(model, queries):
    """
      Make a QuerySet, based on one or more given queries. Delegate each query
      to _query_to_qset and return the intersection of the returned QuerySets.
    """
    def empty_qset(model): return models.query.QuerySet.none(model.objects.all())

    qset = empty_qset(model)#models.query.QuerySet.none(model.objects.all()) # empty QuerySet
    for query in queries.items():
      qset_part = ModelExtension._query_to_qset(model, query)
      if not qset_part:
        # Nothing found, so an empty QuerySet could be returned immediately.
        return empty_qset(model)#models.query.QuerySet.none(model.objects.all())
      elif not qset:
        # First QuerySet has been found.
        qset = qset_part
      else:
        # Another QuerySet has been found, so intersect it with the existing
        # one and check if this intersection is not empty.
        qset &= qset_part
        if not qset:
          # Intersection of QuerySets is empty, so return it immediately.
          return empty_qset(model)#models.query.QuerySet.none(model.objects.all())
    #logger.debug("Queries '%s' gave QuerySet: %s" % (queries,qset))
    return qset

  @staticmethod
  def _query_to_qset(model, query):
    """
      Make a QuerySet, based on a single given query.

      The given query has to be a tuple like:
        ('<attr>','<val>')
        ('<FK>','<val>')
        ('<FK>__<attr>[+<attr>]*','<val>')
    """
    # Split the query to decide which path should be followed. The path depends
    # on the possible elements in the argument.
    attr, val = query
    logger.debug('attr,val: %s,%s' % (attr,val))
    if attr.find('__') is -1:
      fld = model._meta.get_field(attr) # !!! TODO: try, except FieldDoesNotExist !!!
      if isinstance(fld, ForeignKey):
        # So the query was like: '<FK>=<val>'.
        # Now get id's of the objects (of the referenced model) with value in
        # one of its fields.
        to = fld.rel.to
        ids = ModelExtension.search_object_ids(to, val)
        # Finally use a filter with the IN field-lookup, like <attr>__in(<ids>)
        wrapper_cmd = "%s.%s.objects.filter(%s__in=%s)" % (CLUSTER_MODELS, model.__name__, attr, ids)
        logger.debug("Built command to filter '%s': %s" % (query,wrapper_cmd))
        qset = eval(wrapper_cmd)
      else:
        # Then the query was like: '<attr>=<val>'.
        wrapper_cmd = "%s.%s.objects.filter(%s=%s)" % (CLUSTER_MODELS, model.__name__, attr, val)
        logger.debug("Built command to filter '%s': %s" % (query,wrapper_cmd))
        qset = eval(wrapper_cmd)
    else:
      # Argument appearantly was like: '<FK>__<attr>[+<attr>]*=<val>'
      partitioned = attr.partition('__')
      fld = model._meta.get_field(partitioned[0])
      to = fld.rel.to
      attrs = partitioned[2].split('+')
      # Make an empty QuerySet to fill with the union of multiple QuerySets
      qset = models.query.QuerySet.none(to.objects.all())
      for attr in attrs:
        wrapper_cmd = "%s.%s.objects.filter(%s__%s=%s)" % (CLUSTER_MODELS, model.__name__, fld.name, attr, val)
        logger.debug("Built command to filter '%s': %s" % (query,wrapper_cmd))
        # Unite the resulting QuerySet with the so far constructed QuerySet
        qset |= eval(wrapper_cmd)

    #logger.debug("Query '%s' gave QuerySet (with ID's):\n%s (%s)"
    #              % (query,qset,[item.id for item in qset]))
    return qset

      


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


  @staticmethod
  def search_objects(model, value, fields=None):
    """
      Search for objects of the given model. This method will find objects with
      the given value in the (list of) given field(s).
      Returns a list of matching objects.
    """
    matching_indices = ModelExtension.search_object_ids(model, value, fields)
    matches = model.objects.in_bulk(matching_indices)
    objects = matches.values()
    return objects


  @staticmethod
  def objects_from_dict(model, arg_dict):
    """
      Search for objects of the given model. This method will find objects with
      values according to the given dictionary.
    """
    # !!! TODO: Handle<FK>__<attr1>+<attr2>=<val>
    objects_qset = QuerySet()

    for arg in arg_dict:
      if arg == 'id':
        # It's the id-field; Just ignore it.
        logger.debug('Skipping arg with id-field')
        continue
      elif arg.find('__') is -1:
        # Then assume it's a regular field.
        part_qset = entities[entity_type].objects.complex_filter(arg_dict)
      else:
        partitioned = arg.partition('__')
        fk, attr = partitioned[0], partitioned[2]
        fld = self._meta.get_field(fk)
        to = fld.rel.to
        val = arg_dict[arg]

        #part_qset = 

        # !!! TODO: Complete !!!


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

    
  def setattrs_from_dict(self, arg_dict):
    """
      Set attributes according to the arguments, given in a dictionary. Each
      key in the dictionary should match an attribute name in the model. Checks
      are delegated to the _setattr-function.
    """
    for arg in arg_dict:
      if arg == 'id':
        # It's the id-field; Just ignore it.
        logger.debug('Skipping arg with id-field')
        continue
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
      missing = self._missing_fields()
      logger.info('Missing required attributes: %s'
        % ' '.join([field.name for field in missing]))

      current_field = missing[0]
      input = raw_input(current_field.verbose_name+': ')
      try:
        assert bool(input), 'Field cannot be left blank'
        # Input for missing attribute is now stored in variable 'input'.
        i = self._setattr(current_field, input)
        #self.save()
        missing.remove(current_field)
      except AssertionError, err:
        logger.error(err)
      except sqlite3.IntegrityError, err:
        print IntegrityError, err

      logger.info('Current values: %s' % self.__dict__)

      #for field in missing:
      #  input = raw_input(field.verbose_name+': ')
      #  try:
      #    assert bool(input), 'Field cannot be left blank'
      #    # Input for missing attribute is now stored in variable 'input'.
      #    self._setattr(field, input)
      #  except AssertionError, err:
      #    logger.error(err)
      #
      #logger.info('Current values: %s' % self.__dict__)
      #missing = self._missing_fields()


  def _setfk(self, field, value, subfields=None):
    """
      Set the FK of the given field to the id of an entity with the given value
      in one of its required fields (minus 'id' and FKs).
    """
    model = field.rel.to
    objects = ModelExtension.search_objects(model, value, subfields)
    object_count = len(objects)
    if object_count is 0:
      logger.info('No matching object found; Change your query.')
      pass
    elif object_count is 1:
      object = objects.pop()
      self.__setattr__(field.attname, object.id)
      logger.info('%s now references to %s'%(field.name,object))
    else:
      # !!! TODO: let the user refine the search !!!
      logger.info('To many matching objects; Refine your query.')
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

    logger.debug('field=%s (%s), value=%s' % (field.name,field.__class__.__name__,value.__repr__()))

    assert isinstance(value, StringTypes), "Given value is a %s, which isn't supported yet (still have to implement this)" % type(value) # !!! TODO: implement support for lists of values !!!
    if isinstance(field, ForeignKey):
      self._setfk(field, value)
    else:
      self.__setattr__(field.name, value)

    if ModelExtension._is_complete(self):
      try:
        self.save() # !!! TODO: disable at dry-runs
      except (sqlite3.IntegrityError, ValueError), err:
        logger.error(err)

  
#########


  def _filter(self, filter, model_class):
    _model_class = model_class or self.__class__
    items = filter.split(',')
    _dict = {}

    while items:
      item = items.pop(0).split('=')
      _dict[item[0]] = item[1]

    result = _model_class.objects.complex_filter(_dict)
    
    try:
      assert len(result) is 1, "Number of %s matching '%s' is %s (has to be 1)" \
        % (_model_class._meta.verbose_name_plural, filter, len(result))
    except AssertionError, e:
      logger.error(e)
      sys.exit(1)

    return result

##############
