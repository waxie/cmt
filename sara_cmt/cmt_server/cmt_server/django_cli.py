#    This file is part of CMT, a Cluster Management Tool made at SURFsara.
#    Copyright (C) 2012, 2013  Sil Westerveld, Ramon Bastiaans
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
from django.core.exceptions import ValidationError
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ForeignKey, ManyToManyField, \
    OneToOneField, RelatedField

from types import *

import sqlite3
from sqlite3 import IntegrityError

from cmt_server.logger import Logger
logger = Logger().getLogger()

from cmt_server.parser import Parser
parser = Parser().getParser()

from django.db import models

import tagging
from tagging.fields import TagField
from django_extensions.db.fields import CreationDateTimeField, \
                                        ModificationDateTimeField

import settings

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
        import cmt_server.apps.cluster.admin
        admin_list_display = eval('cmt_server.apps.cluster.admin.' \
                                + admin_class_name + '.list_display')

        # Determine longest value-string to display
        longest_key = 0
        for val in admin_list_display:
            if len(val) > longest_key:
                longest_key = len(val)

        # Print the values
        print ' .---[  %s  ]---' % instance
        for key in admin_list_display:
            if key in ('__unicode__', '__str__'):
                continue

            value = instance.__getattribute__(key)
            if type( value ) is MethodType:
                print ' : %s : %s' % (key.ljust(longest_key), value() )
            else:
                print ' : %s : %s' % (key.ljust(longest_key), value )
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

            field_name = arg

            def cmt_validate( f_object, f_name, v_str ):

                if not f_object or not v_str:

                    return

                for v in field.validators:
                        try:
                                v( value )

                        except ValidationError, e:

                                #FIXME: get exception message to display without looking like: [u'message']
                                print 'ERROR: Value "%s" is not valid for %s: %s' %( value, arg, str( e ) )
                                print 'Aborting (value not saved)..'

                                import sys
                                sys.exit( 1 )

            if len( field.validators ) > 0:

                if type( arg_dict[arg] ) in ( ListType, TupleType ):

                    for value in arg_dict[arg]:

                        cmt_validate( field, field_name, value )

                elif type( arg_dict[arg] ) in ( IntType, FloatType, StringType ):

                    cmt_validate( field, field_name, arg_dict[arg] )

                else:
                    logger.debug("Unknown value type '%s' to validate for field: %s" % (str( type(arg_dict[arg]) ), field_name ))

            logger.debug("Have to assign %s to attribute '%s' (%s)" \
                % (arg_dict[arg], arg, field.__class__.__name__))

            # In case of an id-field: Just ignore it.
            if arg == 'id':
                logger.error("Better to not set an id-field, so I'll skip \
                    this one")
                continue

            # Leave M2Ms for later, because they need an object's id
            elif type(field) == ManyToManyField:
                m2ms.append([field, arg_dict[arg]])

            self._setattr(field=arg, value=arg_dict[arg])

        # Save object to give it an id, and make the M2M relations
        if not parser.values.DRYRUN:
            try:
                self.save()
            except Exception as err:
                logger.warning('%s: %s. Maybe not enough (unique) data provided?' % (type(err), err[-1] ))

        for m2m in m2ms:
            self._setm2m(m2m[0], m2m[1])

        if self.is_complete():
            save_msg = 'Saved %s %s' % (self.__class__.__name__, self)
            if not parser.values.DRYRUN:
                try:
                    self.save()
                    logger.info(save_msg)
                except (sqlite3.IntegrityError, ValueError), err: # ??? what if using non-sqlite db? ???
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

        # ??? TODO: Validation via forms:
        #     http://docs.djangoproject.com/en/dev/ref/forms/validation/ ???

        missing = self._missing_fields()

        while missing:
            logger.info('Missing required attributes: %s'
                % ' '.join([field.name for field in missing]))

            current_field = missing[0]
            interactive_input = [raw_input(current_field.verbose_name + ': ')]
            logger.debug('INTERACTIVE INPUT: %s'%interactive_input)
            try:
                assert bool(interactive_input), 'Field cannot be left blank'
                # Input for missing attribute is now stored in var 'input'.
                #i = self._setattr(current_field, input)
                #self.save()
                self._setattr(current_field, interactive_input)
                missing.remove(current_field)
            except AssertionError, err:
                logger.error(err)
            except sqlite3.IntegrityError, err: # ??? what if using non-sqlite db? ???
                logger.error('IntegrityError:', err)

            logger.debug('Current values: %s' % self.__dict__)
            missing = self._missing_fields()

    def _setfk(self, field, value, subfields=None):
        """
            Set the FK of the given field to the id of an object with the
            given value in one of its required fields (minus 'id' and FKs).
        """
        to_model = field.rel.to
        logger.debug("Trying to save '%s' (type:%s) in FK to %s"
            % (value, type(value), to_model.__name__))

        if isinstance(value, StringTypes):
            value = [value]
            logger.debug("Transformed value '%s' in list '%s'"%(value[0], value))

        # determine which fields should be searched for
        if not subfields:
            subfields = to_model()._required_local_fields() # exclude FKs

        logger.debug('Searching a %s matching on fields %s'
            % (to_model.__name__, [f.name for f in subfields]))

        qset = models.query.EmptyQuerySet(model=to_model)
        # OR-filtering QuerySets
        # !!! TODO: have to use Q-objects for this !!!
        # !!! TODO: have to write a Custom Manager for this !!!
        for subfield in subfields:
            # !!! TODO: support multiple values[] !!!
            try:
                found = to_model.objects.filter(
                    **{'%s__in' % subfield.name: value})
                logger.debug('Iteration done, found: %s (%s)'%(found, type(found)))
                # higher priority on the label-field:
                if len(found) == 1 and (subfield.name == 'label' or subfield.name == 'name'):
                    qset = found
                    break
                qset |= found
            except ValueError, e:
                logger.warning(e)
        logger.debug('Found the following matching objects: %s' % qset)

        objects = [_object for _object in qset]
        object_count = len(objects)
        if object_count is 0:
            logger.warning('No matching object found; Change your query.')
        elif object_count is 1:
            _object = objects[0]
            logger.debug('Found 1 match: %s' % _object)
            self.__setattr__(field.attname, _object.id)
            logger.debug('%s now references to %s' % (field.name, _object))
        else:
            # !!! TODO: let the user refine the search !!!
            logger.warning('To many matching objects; Refine your query.')
            # Try the match with the highest number of matches, ...

    def _setm2m(self, field, values, subfields=None):
        """
            Set a ManyToMany-relation.
        """
        to_model = field.rel.to
        logger.debug("Trying to make M2M-relations to %s based on '%s'" \
            % (to_model.__name__, values))

        # determine which fields should be searched for
        if not subfields:
            #subfields = to_model()._required_fields()
            subfields = to_model()._required_local_fields() # exclude FKs

        qset = models.query.EmptyQuerySet(model=to_model)
        # OR-filtering QuerySets
        # !!! TODO: have to write a Custom Manager for this !!!
        for subfield in subfields:
            logger.debug("Searching in field '%s'" % subfield.name)
            qset |= to_model.objects.filter(
                **{'%s__in' % subfield.name: values})
        logger.debug('Found the following matching objects: %s' % qset)

        objects = [_object for _object in qset]
        object_count = len(objects)
        if object_count is 0:
            logger.warning('No matching object found; Change your query.')
            pass
        else:
            for _object in objects:
                # !!! TODO: make options to add (+=), remove(-=), and set (=)
                self.__getattribute__(field.name).add(_object)

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

        logger.debug("Trying to set attribute '%s' (%s) to %s" \
            % (field.name, field.__class__.__name__, value.__repr__()))

        if isinstance(field, ForeignKey):
            self._setfk(field, value)
        elif isinstance(field, ManyToManyField):
            logger.debug("""Found an M2M field. Can't assign it as long as the" \
                object doesn't have an id, so leave this for later""")
        else:
            logger.debug('Trying to set attribute of %s'%type(field))
            for e in value: # iterate through all elements
                self.__setattr__(field.name, e)
            if len(value) > 1:
                # !!! TODO: append values, instead of overwrite !!!
                # like: for v in value: self.<append>(v)
                logger.debug('Functionality to append values is still missing')


class ObjectManager():
    """
        The ObjectManager is responsible for operations on objects in the
        database.
        Operations are based on a given Query-object.
    """

    def __init__(self):
        logger.debug('Initializing ObjectManager')

    def get_objects(self, query):
        """
            Retrieve objects from the database, corresponding to the entity
            and terms in the given query. The terms are OR-ed by default.
        """
        # !!! TODO: Implement AND !!!
        kwargs = {}

        logger.debug('CHECK query: %s' % query)
        for attr, val in query['get'].items():
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
                sys.exit(1)

        objects = query['ent'].objects.filter(**kwargs)
        return objects.distinct()

    def save_objects(self, qset):
        """
            Save all objects of the given QuerySet.
        """
        # TODO: implement
        for _object in qset:
            try:
                self._save_object(_object)
            except:
                logger.error('Error saving %s %s' \
                    % (_object.__class__.__name__, _object))

    def display(self, instance):
        """
            Print all values
        """
        # TODO: implement
        pass


class QueryManager():
    """
        The QueryManager has knowledge about building Queries based on
        arguments that are given on the commandline. Those arguments can be
        pushed to the QueryManager with push_args(), which on its turn will
        build a new Query, which can be retrieved with get_query().
    """

    def __init__(self):
        logger.debug('Initializing QueryManager')
        self.query = self.Query()

    class Query(dict):
        """
            Query holds a dictionary of the given args.
        """

        def __init__(self, ent=None):
            logger.debug('Initializing new Query')
            if ent:
                self._new(ent)

        def _new(self, ent=None):
            self['ent'] = ent
            self['get'] = {}
            self['set'] = {}
            # ??? TODO: maybe implement something like `self['fields'] = {}`
            #     to narrow the searchspace ???

    def push_args(self, args, entity, keys=['default']):
        """
            # args = list of args from cli, like:
            #     ['get', 'label=fs7', 'label=fs6']
            # entity = class of given entity, like:
            #     <class 'cmt_server.apps.cluster.models.HardwareUnit'>
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

        logger.debug("push_args built query '%s'" % self.query)

    def get_query(self):
        return self.query
