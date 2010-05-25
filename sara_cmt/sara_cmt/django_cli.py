from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignKey, ManyToManyField, \
    OneToOneField, RelatedField

from types import StringTypes

import sqlite3
from sqlite3 import IntegrityError

from sara_cmt.logger import Logger
logger = Logger().getLogger()

from sara_cmt.parser import Parser
parser = Parser().getParser()

from django.db import models

import tagging
from tagging.fields import TagField
from django_extensions.db.fields import CreationDateTimeField, \
                                        ModificationDateTimeField

# To be able to migrate fields of 3rd party app django-extensions
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_extensions\.db\.fields"])


class ModelExtension(models.Model):
    """
        The ModelExtension of Django-CLI is meant as a Mixin for a Django
        Model.
    """
    tags = TagField()
    created_on = CreationDateTimeField()
    updated_on = ModificationDateTimeField()
    note = models.TextField(blank=True)

    class Meta:
        abstract = True


#####
#
# <STATIC METHODS>
#

    @staticmethod
    def display(instance):
        """
            Print all values given in list_display of the model's admin
        """
        # First get access to the admin
        admin_class_name = instance._meta.object_name + 'Admin'
        import sara_cmt.cluster.admin
        admin_list_display = eval('sara_cmt.cluster.admin.' \
                                + admin_class_name + '.list_display')

        # Determine longest value-string to display
        longest_key = 0
        for val in admin_list_display:
            if len(val) > longest_key:
                longest_key = len(val)

        # Print the values
        print ' .---[  %s  ]---' % instance
        for key in admin_list_display:
            if key not in ('__unicode__', '__str__'):
                print ' : %s : %s' % (key.ljust(longest_key), \
                                      instance.__getattribute__(key))
        print " '---\n"
#
# </STATIC METHODS>
#
#####

    def _required_fields(self):
        """
            Checks which fields are required, and returns these fields in a
            set.
        """
        fields = [fld for fld in self._meta.fields if not fld.blank]
        return fields

    def _required_local_fields(self):
        """
            Checks which local fields are required, and returns these fields
            in a set. A local field can be of any type except ForeignKey and
            ManyToManyField.
        """
        fields = [fld for fld in self._required_fields() if \
            not isinstance(fld, RelatedField)]
        return fields

    def _required_refering_fields(self):
        """
            Checks which refering fields are required, and returns these
            fields in a set. A refering field is of the type ForeignKey or
            ManyToManyField.
        """
        fields = [fld for fld in self._required_fields() if \
            isinstance(fld, RelatedField)]
        return fields

    def _is_fk(self, field):
        """
            Checks if a given field is a ForeignKey.
            Returns a boolean value.
        """
        # First be sure that we check a field
        if isinstance(field, StringTypes):
            field = self._meta.get_field(field)
            logger.warning('Checking for a ForeignKey with the \
                string-representation of a field')
        retval = isinstance(field, ForeignKey)
        return retval

    def _is_m2m(self, field):
        """
            Checks if a given field is a ManyToManyField.
            Returns a boolean value.
        """
        # First be sure that we check a field
        if isinstance(field, StringTypes):
            field = self._meta.get_field(field)
            logger.warning('Checking for a ManyToMany with the \
                string-representation of a field')
        retval = isinstance(field, ManyToManyField)
        return retval

    def is_complete(self):
        """
            Check if all the required fields has been assigned.
        """
        return not self._missing_fields()

    def setattrs_from_dict(self, arg_dict):
        """
            Set attributes according to the arguments, given in a dictionary.
            Each key in the dictionary should match a fieldname in the model.
        """
        m2ms = [] # to collect M2Ms (which should be done at last)
        for arg in arg_dict:
            field = self._meta.get_field(arg)
            logger.debug("Have to assign %s to attribute '%s' (%s)" \
                % (arg_dict[arg], arg, field.__class__.__name__))

            # In case of an id-field: Just ignore it.
            if arg == 'id':
                logger.error("Better to not set an id-field, so I'll skip \
                    this one")
                continue

            if type(field) == ForeignKey:
                self._setfk(field, arg_dict[arg])

            elif type(field) == ManyToManyField:
                # Leave M2Ms for later, because they need an object's id
                m2ms.append([field, arg_dict[arg]])

            else:
                logger.debug("Assuming '%s' is a regular field" % arg)
                self._setattr(field=arg, value=arg_dict[arg])

        # Save object to give it an id, and make the M2M relations
        if not parser.values.DRYRUN:
            self.save()

        for m2m in m2ms:
            self._setm2m(m2m[0], m2m[1])

        if self.is_complete():
            save_msg = 'Saved %s %s' % (self.__class__.__name__, self)
            if not parser.values.DRYRUN:
                try:
                    self.save()
                    logger.info(save_msg)
                except (sqlite3.IntegrityError, ValueError), err:
                    logger.error(err)
            else:
                logger.info('[DRYRUN] %s' % save_msg)

        logger.debug('attrs_from_dict(%s) => %s' % (arg_dict, self.__dict__))

    def _missing_fields(self):
        """
            Checks if the required fields all have a value assigned to it, to
            be sure it can be saved to the database.
            Returns the set of missing editable fields.
        """
        required, missing = self._required_fields(), []

        # Isolate all missing fields from required fields.
        for field in required:
            try:
                if not self.__getattribute__(field.name) and field.editable:
                    # Field hasn't been set
                    missing.append(field)
            except:
                # FK hasn't been set
                missing.append(field)
        return missing

    def interactive_completion(self):
        """
            Lets the user assign values to the missing fields, by iterating
            over the missing fields. Iteration will stop when all required
            fields are given.
        """
        # !!! Note: This function should only be called in INTERACTIVE mode !!!
        # ??? TODO: Check raw_input for ValueError. ???

        # !!! TODO: Validation via forms:
        #     http://docs.djangoproject.com/en/dev/ref/forms/validation/ !!!

        missing = self._missing_fields()

        while missing:
            logger.info('Missing required attributes: %s'
                % ' '.join([field.name for field in missing]))

            current_field = missing[0]
            input = raw_input(current_field.verbose_name + ': ')
            try:
                assert bool(input), 'Field cannot be left blank'
                # Input for missing attribute is now stored in var 'input'.
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
            Set the FK of the given field to the id of an object with the
            given value in one of its required fields (minus 'id' and FKs).
        """
        to_model = field.rel.to
        #values = value[0].split(',') #
        logger.debug("Trying to save '%s' in FK to %s"
            % (value, to_model.__name__))

        # determine which fields should be searched for
        if not subfields:
            subfields = to_model()._required_local_fields() # exclude FKs

        logger.debug('Searching a %s matching on fields %s'
            % (to_model.__name__, [f.name for f in subfields]))

        qset = models.query.EmptyQuerySet(model=to_model)
        # OR-filtering QuerySets
        # !!! TODO: have to write a Custom Manager for this !!!
        for subfield in subfields:
            # !!! TODO: support multiple values[] !!!
            try:
                found = to_model.objects.filter(
                    **{'%s__in' % subfield.name: value})
                # higher priority on the label-field:
                if len(found) == 1 and subfield.name == 'label':
                    qset = found
                    break
                qset |= found
            except ValueError, e:
                logger.warning(e)
        logger.debug('Found the following matching objects: %s' % qset)

        objects = [object for object in qset]
        object_count = len(objects)
        if object_count is 0:
            logger.warning('No matching object found; Change your query.')
            pass
        elif object_count is 1:
            object = objects[0]
            logger.debug('Found 1 match: %s' % object)
            self.__setattr__(field.attname, object.id)
            logger.debug('%s now references to %s' % (field.name, object))
        else:
            # !!! TODO: let the user refine the search !!!
            logger.warning('To many matching objects; Refine your query.')
            # Try the match with the highest number of matches, ...
            pass

    def _setm2m(self, field, value, subfields=None):
        """
            Set a ManyToMany-relation.
        """
        to_model = field.rel.to
        values = value[0].split(',')
        logger.debug("Trying to make M2M-relations to %s based on '%s'" \
            % (to_model.__name__, value))

        # determine which fields should be searched for
        if not subfields:
            #subfields = to_model()._required_fields()
            subfields = to_model()._required_local_fields() # exclude FKs

        logger.debug('Searching a %s matching on fields %s' \
            % (to_model.__name__, [f.name for f in subfields]))

        qset = models.query.EmptyQuerySet(model=to_model)
        # OR-filtering QuerySets
        # !!! TODO: have to write a Custom Manager for this !!!
        for subfield in subfields:
            logger.critical('searching in field: %s' % subfield.name)
            qset |= to_model.objects.filter(
                **{'%s__in' % subfield.name: values})
        logger.debug('Found the following matching objects: %s' % qset)

        objects = [object for object in qset]
        object_count = len(objects)
        if object_count is 0:
            logger.warning('No matching object found; Change your query.')
            pass
        else:
            for object in objects:
                self.__getattribute__(field.name).add(object)

        logger.critical('value to save: %s' % value)


        pass

    def _setattr(self, field, value):
        """
            Assign the given value to the attribute belonging to the given
            field. The field can be given as a field in the model, or as the
            string matching its name.
            When given as a string, it may be followed by '__<attr>', to
            search for already existing entities with the <attr>-field equal
            to the given value.
            If the search results to a single match, the id of the matching
            entity is assigned to the given ForeignKey-field.
        """
        # First init the field itself if it's given as a string
        if isinstance(field, StringTypes):
            field = self._meta.get_field(field)


        # !!! TODO: Quick {che,ha}ck; have to check this once more !!!
        if isinstance(value, list):
            value = value[0]

        logger.debug("Trying to set attribute '%s' (%s) to %s" \
            % (field.name, field.__class__.__name__, value.__repr__()))

        # !!! TODO: implement support for lists of values !!!
        assert isinstance(value, StringTypes), "Given value is a %s, which \
            isn't supported yet (still have to implement this)" % type(value)
        if isinstance(field, ForeignKey):
            self._setfk(field, value)
        elif isinstance(field, ManyToManyField):
            logger.debug('We found a M2M field, but first have to implement \
                a function to handle this')
            pass
            # !!! TODO: Implement M2M relations !!!
        else:
            #logger.debug('We have to handle a %s'%type(field))
            self.__setattr__(field.name, value)


class ObjectManager():
    """
        The ObjectManager is responsible for operations on objects in the
        database.
        Operations are based on a given Query-object.
    """

    def __init__(self):
        logger.info('Initializing ObjectManager')

    def get_objects(self, query):
        """
            Retrieve objects from the database, corresponding to the entity
            and terms in the given query. The terms are OR-ed by default.
        """
        # !!! TODO: Implement AND !!!
        kwargs = {}

        for attr, val in query['get'].items():
            logger.debug('CHECK query: %s' % query)
            try:
                fld = query['ent']._meta.get_field(attr)
                logger.debug('CHECK %s: %s' \
                    % (fld.__class__.__name__, fld.name))
                if type(fld) in (ForeignKey, ManyToManyField):
                    # Default field to search in
                    if 'label' in fld.rel.to().__dict__:
                        label = 'label'
                    else:
                        label = 'name'
                    # ??? TODO: maybe use %s__str ???
                    attr = '%s__%s' % (attr, label)
                kwargs['%s__in' % attr] = val
            except FieldDoesNotExist, err:
                logger.error(err)

        objects = query['ent'].objects.filter(**kwargs)
        return objects

    def save_objects(self, qset):
        """
            Save all objects of the given QuerySet.
        """
        # TODO: implement
        for object in qset:
            try:
                self._save_object(object)
            except:
                logger.error('Error saving %s %s' \
                    % (object.__class__.__name__, object))

    def display(self, instance):
        """
            Print all values
        """
        pass


class QueryManager():
    """
        The QueryManager has knowledge about building Queries based on
        arguments that are given on the commandline. Those arguments can be
        pushed to the QueryManager with push_args(), which on its turn will
        build a new Query, which can be retrieved with get_query().
    """

    def __init__(self):
        logger.info('Initializing QueryManager')
        self.query = self.Query()

    class Query(dict):
        """
            Query holds a dictionary of the given args.
        """

        def __init__(self, ent=None):
            logger.info('Initializing new Query')
            if ent:
                self._new(ent)

        def _new(self, ent=None):
            self['ent'] = ent
            self['get'] = {}
            self['set'] = {}
            # ??? TODO: maybe implement something like `self['fields'] = {}`
            #     to narrow the searchspace ???

        def as_tuple(self):
            """
                Returns a tuple of tuples. Those tuples are based on the the
                items from the output of queries_to_dict(queries). Example:

                {'hostname':'node1', 'rack':['3', '4']}

                should become

                (('hostname', 'node1'), ('rack', ('3', '4')))
            """
            # TODO: implement function which converts a (nested) dict into a
            #       (nested) tuple
            pass

        def as_list(self):
            """
                Returns a list of lists. Those lists are based on the items
                from the output of queries_to_dict(queries). For example:

                {'hostname':'node1', 'rack':['3', '4']}

                should become

                [['hostname', 'node1'], ['rack', ['3', '4']]]
            """
            # TODO: implement function which converts a (nested) dict into a
            #       (nested) list
            pass

    def push_args(self, args, entity, keys=['default']):
        """
            # args = list of args from cli, like:
            #     ['get', 'label=fs7', 'label=fs6']
            # entity = class of given entity, like:
            #     <class 'sara_cmt.cluster.models.HardwareUnit'>
            # keys = the key(s) to use (which depends on the given option),
            # like:
            #     ['get']
        """
        self.query = self.Query(entity)

        key = keys[0]

        for arg in args:
            #logger.debug("checking arg '%s' of args '%s'"%(arg,args))
            if arg in keys: # it's a key like 'get', 'set'
                key = arg
            else: # it's an assignment like 'label=fs6'
                attr, val = arg.split('=', 1)

                if attr in self.query[key]:
                    # this isn't the first time we see this attribute, so
                    # assign an extra value to it
                    self.query[key][attr].append(val)
                else:
                    # this is the first time we see this attribute
                    self.query[key][attr] = [val]

        logger.debug("push_args built query '%s' from args '%s'" \
            % (self.query, args))

    def get_query(self):
        return self.query
