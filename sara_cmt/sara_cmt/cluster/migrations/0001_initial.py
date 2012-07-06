# encoding: utf-8

#    This file is part of CMT, a Cluster Management Tool made at SARA.
#    Copyright (C) 2012  Sil Westerveld
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

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cluster'
        db.create_table('cluster_cluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('cluster', ['Cluster'])

        # Adding model 'HardwareUnit'
        db.create_table('cluster_hardwareunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hardware', to=orm['cluster.Cluster'])),
            ('specifications', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hardware', blank=True, null=True, to=orm['cluster.HardwareModel'])),
            ('warranty', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hardware', blank=True, null=True, to=orm['cluster.WarrantyContract'])),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contents', to=orm['cluster.Rack'])),
            ('serialnumber', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('service_tag', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('first_slot', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['HardwareUnit'])

        # Adding unique constraint on 'HardwareUnit', fields ['rack', 'first_slot']
        db.create_unique('cluster_hardwareunit', ['rack_id', 'first_slot'])

        # Adding M2M table for field role on 'HardwareUnit'
        db.create_table('cluster_hardwareunit_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hardwareunit', models.ForeignKey(orm['cluster.hardwareunit'], null=False)),
            ('role', models.ForeignKey(orm['cluster.role'], null=False))
        ))
        db.create_unique('cluster_hardwareunit_role', ['hardwareunit_id', 'role_id'])

        # Adding model 'Alias'
        db.create_table('cluster_alias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('cluster', ['Alias'])

        # Adding model 'Interface'
        db.create_table('cluster_interface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.Network'])),
            ('hardware', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.HardwareUnit'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.InterfaceType'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hwaddress', self.gf('django.db.models.fields.CharField')(max_length=17, unique=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('cluster', ['Interface'])

        # Adding M2M table for field aliasses on 'Interface'
        db.create_table('cluster_interface_aliasses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('interface', models.ForeignKey(orm['cluster.interface'], null=False)),
            ('alias', models.ForeignKey(orm['cluster.alias'], null=False))
        ))
        db.create_unique('cluster_interface_aliasses', ['interface_id', 'alias_id'])

        # Adding model 'Network'
        db.create_table('cluster_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('netaddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('netmask', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vlan', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3, null=True, blank=True)),
            ('hostnames', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['Network'])

        # Adding model 'Rack'
        db.create_table('cluster_rack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='racks', to=orm['cluster.Room'])),
            ('label', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('cluster', ['Rack'])

        # Adding model 'Country'
        db.create_table('cluster_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('country_code', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
        ))
        db.send_create_signal('cluster', ['Country'])

        # Adding model 'Address'
        db.create_table('cluster_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='addresses', blank=True, null=True, to=orm['cluster.Country'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['Address'])

        # Adding unique constraint on 'Address', fields ['address', 'city']
        db.create_unique('cluster_address', ['address', 'city'])

        # Adding model 'Room'
        db.create_table('cluster_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rooms', to=orm['cluster.Address'])),
            ('floor', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['Room'])

        # Adding unique constraint on 'Room', fields ['address', 'floor', 'label']
        db.create_unique('cluster_room', ['address_id', 'floor', 'label'])

        # Adding model 'Site'
        db.create_table('cluster_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('cluster', ['Site'])

        # Adding model 'Company'
        db.create_table('cluster_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('cluster', ['Company'])

        # Adding M2M table for field addresses on 'Company'
        db.create_table('cluster_company_addresses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm['cluster.company'], null=False)),
            ('address', models.ForeignKey(orm['cluster.address'], null=False))
        ))
        db.create_unique('cluster_company_addresses', ['company_id', 'address_id'])

        # Adding model 'Connection'
        db.create_table('cluster_connection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='connections', to=orm['cluster.Address'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='companies', to=orm['cluster.Company'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('cluster', ['Connection'])

        # Adding unique constraint on 'Connection', fields ['company', 'name']
        db.create_unique('cluster_connection', ['company_id', 'name'])

        # Adding model 'Telephonenumber'
        db.create_table('cluster_telephonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='telephone_numbers', to=orm['cluster.Country'])),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='telephone_numbers', to=orm['cluster.Connection'])),
            ('areacode', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('subscriber_number', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('cluster', ['Telephonenumber'])

        # Adding model 'HardwareModel'
        db.create_table('cluster_hardwaremodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model specifications', to=orm['cluster.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('rackspace', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('expansions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('cluster', ['HardwareModel'])

        # Adding model 'Role'
        db.create_table('cluster_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('cluster', ['Role'])

        # Adding model 'InterfaceType'
        db.create_table('cluster_interfacetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', blank=True, null=True, to=orm['cluster.Company'])),
        ))
        db.send_create_signal('cluster', ['InterfaceType'])

        # Adding model 'WarrantyType'
        db.create_table('cluster_warrantytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warranty types', to=orm['cluster.Connection'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('cluster', ['WarrantyType'])

        # Adding model 'WarrantyContract'
        db.create_table('cluster_warrantycontract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('created_on', self.gf('django_extensions.db.fields.CreationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django_extensions.db.fields.ModificationDateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contracts', blank=True, null=True, to=orm['cluster.WarrantyType'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('cluster', ['WarrantyContract'])


    def backwards(self, orm):
        
        # Deleting model 'Cluster'
        db.delete_table('cluster_cluster')

        # Deleting model 'HardwareUnit'
        db.delete_table('cluster_hardwareunit')

        # Removing unique constraint on 'HardwareUnit', fields ['rack', 'first_slot']
        db.delete_unique('cluster_hardwareunit', ['rack_id', 'first_slot'])

        # Removing M2M table for field role on 'HardwareUnit'
        db.delete_table('cluster_hardwareunit_role')

        # Deleting model 'Alias'
        db.delete_table('cluster_alias')

        # Deleting model 'Interface'
        db.delete_table('cluster_interface')

        # Removing M2M table for field aliasses on 'Interface'
        db.delete_table('cluster_interface_aliasses')

        # Deleting model 'Network'
        db.delete_table('cluster_network')

        # Deleting model 'Rack'
        db.delete_table('cluster_rack')

        # Deleting model 'Country'
        db.delete_table('cluster_country')

        # Deleting model 'Address'
        db.delete_table('cluster_address')

        # Removing unique constraint on 'Address', fields ['address', 'city']
        db.delete_unique('cluster_address', ['address', 'city'])

        # Deleting model 'Room'
        db.delete_table('cluster_room')

        # Removing unique constraint on 'Room', fields ['address', 'floor', 'label']
        db.delete_unique('cluster_room', ['address_id', 'floor', 'label'])

        # Deleting model 'Site'
        db.delete_table('cluster_site')

        # Deleting model 'Company'
        db.delete_table('cluster_company')

        # Removing M2M table for field addresses on 'Company'
        db.delete_table('cluster_company_addresses')

        # Deleting model 'Connection'
        db.delete_table('cluster_connection')

        # Removing unique constraint on 'Connection', fields ['company', 'name']
        db.delete_unique('cluster_connection', ['company_id', 'name'])

        # Deleting model 'Telephonenumber'
        db.delete_table('cluster_telephonenumber')

        # Deleting model 'HardwareModel'
        db.delete_table('cluster_hardwaremodel')

        # Deleting model 'Role'
        db.delete_table('cluster_role')

        # Deleting model 'InterfaceType'
        db.delete_table('cluster_interfacetype')

        # Deleting model 'WarrantyType'
        db.delete_table('cluster_warrantytype')

        # Deleting model 'WarrantyContract'
        db.delete_table('cluster_warrantycontract')


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
            'Meta': {'unique_together': "(('rack', 'first_slot'),)", 'object_name': 'HardwareUnit'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'to': "orm['cluster.Cluster']"}),
            'created_on': ('django_extensions.db.fields.CreationDateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_slot': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'through': "orm['cluster.Interface']", 'to': "orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': "orm['cluster.Rack']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'to': "orm['cluster.Role']"}),
            'serialnumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'service_tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
