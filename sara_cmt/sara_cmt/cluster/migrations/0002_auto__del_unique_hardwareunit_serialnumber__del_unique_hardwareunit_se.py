# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'HardwareUnit', fields ['serialnumber']
        db.delete_unique('cluster_hardwareunit', ['serialnumber'])

        # Removing unique constraint on 'HardwareUnit', fields ['service_tag']
        db.delete_unique('cluster_hardwareunit', ['service_tag'])

        # Adding unique constraint on 'HardwareUnit', fields ['serialnumber', 'service_tag']
        db.create_unique('cluster_hardwareunit', ['serialnumber', 'service_tag'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'HardwareUnit', fields ['serialnumber']
        db.create_unique('cluster_hardwareunit', ['serialnumber'])

        # Adding unique constraint on 'HardwareUnit', fields ['service_tag']
        db.create_unique('cluster_hardwareunit', ['service_tag'])

        # Removing unique constraint on 'HardwareUnit', fields ['serialnumber', 'service_tag']
        db.delete_unique('cluster_hardwareunit', ['serialnumber', 'service_tag'])


    models = {
        'cluster.address': {
            'Meta': {'unique_together': "(('address', 'city'),)", 'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.Country']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.alias': {
            'Meta': {'object_name': 'Alias'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.company': {
            'Meta': {'object_name': 'Company'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'_companies'", 'to': "orm['cluster.Address']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cluster.connection': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Connection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connections'", 'to': "orm['cluster.Address']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'companies'", 'to': "orm['cluster.Company']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.country': {
            'Meta': {'object_name': 'Country'},
            'country_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.hardwaremodel': {
            'Meta': {'object_name': 'HardwareModel'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expansions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rackspace': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model specifications'", 'to': "orm['cluster.Company']"})
        },
        'cluster.hardwareunit': {
            'Meta': {'unique_together': "(('rack', 'first_slot'), ('serialnumber', 'service_tag'))", 'object_name': 'HardwareUnit'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'to': "orm['cluster.Cluster']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_slot': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'through': "orm['cluster.Interface']", 'to': "orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': "orm['cluster.Rack']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'to': "orm['cluster.Role']"}),
            'serialnumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'service_tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'specifications': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.HardwareModel']"}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'warranty': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.WarrantyContract']"})
        },
        'cluster.interface': {
            'Meta': {'object_name': 'Interface'},
            'aliasses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'_interfaces'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.Alias']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hardware': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.HardwareUnit']"}),
            'hwaddress': ('django.db.models.fields.CharField', [], {'max_length': '17', 'unique': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.InterfaceType']"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.interfacetype': {
            'Meta': {'object_name': 'InterfaceType'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.Company']"})
        },
        'cluster.network': {
            'Meta': {'object_name': 'Network'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hostnames': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'netaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'netmask': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        'cluster.rack': {
            'Meta': {'object_name': 'Rack'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'racks'", 'to': "orm['cluster.Room']"}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.role': {
            'Meta': {'object_name': 'Role'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.room': {
            'Meta': {'unique_together': "(('address', 'floor', 'label'),)", 'object_name': 'Room'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rooms'", 'to': "orm['cluster.Address']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.site': {
            'Meta': {'object_name': 'Site'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.telephonenumber': {
            'Meta': {'object_name': 'Telephonenumber'},
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': "orm['cluster.Connection']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': "orm['cluster.Country']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subscriber_number': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.warrantycontract': {
            'Meta': {'object_name': 'WarrantyContract'},
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contracts'", 'blank': 'True', 'null': 'True', 'to': "orm['cluster.WarrantyType']"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.warrantytype': {
            'Meta': {'object_name': 'WarrantyType'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warranty types'", 'to': "orm['cluster.Connection']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'updated_on': ('django_extensions.db.fields.ModificationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['cluster']
