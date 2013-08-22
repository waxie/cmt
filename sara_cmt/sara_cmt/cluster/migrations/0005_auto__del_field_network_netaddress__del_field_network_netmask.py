# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Network.netaddress'
        db.delete_column(u'cluster_network', 'netaddress')

        # Deleting field 'Network.netmask'
        db.delete_column(u'cluster_network', 'netmask')


    def backwards(self, orm):
        # Adding field 'Network.netaddress'
        db.add_column(u'cluster_network', 'netaddress',
                      self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15),
                      keep_default=False)

        # Adding field 'Network.netmask'
        db.add_column(u'cluster_network', 'netmask',
                      self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15),
                      keep_default=False)


    models = {
        u'cluster.address': {
            'Meta': {'ordering': "('postalcode',)", 'unique_together': "(('address', 'city'),)", 'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'addresses'", 'null': 'True', 'to': u"orm['cluster.Country']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.cluster': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Cluster'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machinenames': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.company': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Company'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'_companies'", 'symmetrical': 'False', 'to': u"orm['cluster.Address']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'cluster.connection': {
            'Meta': {'ordering': "('company', 'address')", 'unique_together': "(('company', 'name'),)", 'object_name': 'Connection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'connections'", 'null': 'True', 'to': u"orm['cluster.Address']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'companies'", 'to': u"orm['cluster.Company']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'country_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.hardwaremodel': {
            'Meta': {'ordering': "('vendor', 'name')", 'object_name': 'HardwareModel'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expansions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rackspace': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model specifications'", 'to': u"orm['cluster.Company']"}),
            'vendorcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cluster.hardwareunit': {
            'Meta': {'ordering': "('rack__label', 'first_slot')", 'unique_together': "(('rack', 'first_slot'), ('cluster', 'label'))", 'object_name': 'HardwareUnit'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'to': u"orm['cluster.Cluster']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_slot': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'symmetrical': 'False', 'through': u"orm['cluster.Interface']", 'to': u"orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owns'", 'null': 'True', 'to': u"orm['cluster.Connection']"}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': u"orm['cluster.Rack']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'symmetrical': 'False', 'to': u"orm['cluster.Role']"}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sold'", 'null': 'True', 'to': u"orm['cluster.Connection']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'specifications': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hardware'", 'null': 'True', 'to': u"orm['cluster.HardwareModel']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'warranty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hardware'", 'null': 'True', 'to': u"orm['cluster.WarrantyContract']"}),
            'warranty_tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'cluster.interface': {
            'Meta': {'ordering': "('host__cluster__name', 'host__rack__label', 'host__first_slot')", 'unique_together': "(('network', 'hwaddress'),)", 'object_name': 'Interface'},
            'aliases': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': u"orm['cluster.HardwareUnit']"}),
            'hwaddress': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iftype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': u"orm['cluster.InterfaceType']"}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': u"orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.interfacetype': {
            'Meta': {'ordering': "('label',)", 'object_name': 'InterfaceType'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'interfaces'", 'null': 'True', 'to': u"orm['cluster.Company']"})
        },
        u'cluster.network': {
            'Meta': {'ordering': "('name', 'domain')", 'object_name': 'Network'},
            'cidr': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gateway': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'blank': 'True'}),
            'hostnames': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        u'cluster.rack': {
            'Meta': {'ordering': "('label',)", 'unique_together': "(('room', 'label'),)", 'object_name': 'Rack'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'racks'", 'to': u"orm['cluster.Room']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.role': {
            'Meta': {'ordering': "('label',)", 'object_name': 'Role'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.room': {
            'Meta': {'ordering': "('address__postalcode', 'floor')", 'unique_together': "(('address', 'floor', 'label'),)", 'object_name': 'Room'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rooms'", 'to': u"orm['cluster.Address']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.telephonenumber': {
            'Meta': {'ordering': "('connection',)", 'object_name': 'Telephonenumber'},
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': u"orm['cluster.Connection']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': u"orm['cluster.Country']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subscriber_number': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'cluster.warrantycontract': {
            'Meta': {'ordering': "('label',)", 'object_name': 'WarrantyContract'},
            'annual_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'warranty_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contracts'", 'null': 'True', 'to': u"orm['cluster.WarrantyType']"})
        },
        u'cluster.warrantytype': {
            'Meta': {'ordering': "('contact__company__name', 'label')", 'object_name': 'WarrantyType'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warranty types'", 'to': u"orm['cluster.Connection']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['cluster']
