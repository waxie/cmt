# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cluster'
        db.create_table('cluster_cluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('cluster', ['Cluster'])

        # Adding model 'HardwareUnit'
        db.create_table('cluster_hardwareunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hardware', to=orm['cluster.Cluster'])),
            ('specifications', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='hardware', null=True, to=orm['cluster.HardwareModel'])),
            ('warranty', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='hardware', null=True, to=orm['cluster.WarrantyContract'])),
            ('rack', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contents', to=orm['cluster.Rack'])),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sold', null=True, to=orm['cluster.Connection'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owns', null=True, to=orm['cluster.Connection'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=10, null=True, blank=True)),
            ('warranty_tag', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('first_slot', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
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

        # Adding model 'Interface'
        db.create_table('cluster_interface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.Network'])),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.HardwareUnit'])),
            ('iftype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interfaces', to=orm['cluster.InterfaceType'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('aliases', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('hwaddress', self.gf('django.db.models.fields.CharField')(max_length=17, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
        ))
        db.send_create_signal('cluster', ['Interface'])

        # Adding unique constraint on 'Interface', fields ['network', 'hwaddress']
        db.create_unique('cluster_interface', ['network_id', 'hwaddress'])

        # Adding model 'Network'
        db.create_table('cluster_network', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('netaddress', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('netmask', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('gateway', self.gf('django.db.models.fields.IPAddressField')(max_length=15, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vlan', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=3, null=True, blank=True)),
            ('hostnames', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['Network'])

        # Adding model 'Rack'
        db.create_table('cluster_rack', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='racks', to=orm['cluster.Room'])),
            ('label', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('cluster', ['Rack'])

        # Adding unique constraint on 'Rack', fields ['room', 'label']
        db.create_unique('cluster_rack', ['room_id', 'label'])

        # Adding model 'Country'
        db.create_table('cluster_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('country_code', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
        ))
        db.send_create_signal('cluster', ['Country'])

        # Adding model 'Address'
        db.create_table('cluster_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='addresses', null=True, to=orm['cluster.Country'])),
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
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rooms', to=orm['cluster.Address'])),
            ('floor', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['Room'])

        # Adding unique constraint on 'Room', fields ['address', 'floor', 'label']
        db.create_unique('cluster_room', ['address_id', 'floor', 'label'])

        # Adding model 'Company'
        db.create_table('cluster_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
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
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='connections', null=True, to=orm['cluster.Address'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='companies', to=orm['cluster.Company'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal('cluster', ['Connection'])

        # Adding unique constraint on 'Connection', fields ['company', 'name']
        db.create_unique('cluster_connection', ['company_id', 'name'])

        # Adding model 'Telephonenumber'
        db.create_table('cluster_telephonenumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='telephone_numbers', to=orm['cluster.Country'])),
            ('connection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='telephone_numbers', to=orm['cluster.Connection'])),
            ('areacode', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('subscriber_number', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('number_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('cluster', ['Telephonenumber'])

        # Adding model 'HardwareModel'
        db.create_table('cluster_hardwaremodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='model specifications', to=orm['cluster.Company'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('vendorcode', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('rackspace', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('expansions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('cluster', ['HardwareModel'])

        # Adding model 'Role'
        db.create_table('cluster_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('cluster', ['Role'])

        # Adding model 'InterfaceType'
        db.create_table('cluster_interfacetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='interfaces', null=True, to=orm['cluster.Company'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cluster', ['InterfaceType'])

        # Adding model 'WarrantyType'
        db.create_table('cluster_warrantytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warranty types', to=orm['cluster.Connection'])),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('cluster', ['WarrantyType'])

        # Adding model 'WarrantyContract'
        db.create_table('cluster_warrantycontract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('warranty_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contracts', null=True, to=orm['cluster.WarrantyType'])),
            ('contract_number', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
            ('annual_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('cluster', ['WarrantyContract'])


    def backwards(self, orm):
        # Removing unique constraint on 'Connection', fields ['company', 'name']
        db.delete_unique('cluster_connection', ['company_id', 'name'])

        # Removing unique constraint on 'Room', fields ['address', 'floor', 'label']
        db.delete_unique('cluster_room', ['address_id', 'floor', 'label'])

        # Removing unique constraint on 'Address', fields ['address', 'city']
        db.delete_unique('cluster_address', ['address', 'city'])

        # Removing unique constraint on 'Rack', fields ['room', 'label']
        db.delete_unique('cluster_rack', ['room_id', 'label'])

        # Removing unique constraint on 'Interface', fields ['network', 'hwaddress']
        db.delete_unique('cluster_interface', ['network_id', 'hwaddress'])

        # Removing unique constraint on 'HardwareUnit', fields ['rack', 'first_slot']
        db.delete_unique('cluster_hardwareunit', ['rack_id', 'first_slot'])

        # Deleting model 'Cluster'
        db.delete_table('cluster_cluster')

        # Deleting model 'HardwareUnit'
        db.delete_table('cluster_hardwareunit')

        # Removing M2M table for field role on 'HardwareUnit'
        db.delete_table('cluster_hardwareunit_role')

        # Deleting model 'Interface'
        db.delete_table('cluster_interface')

        # Deleting model 'Network'
        db.delete_table('cluster_network')

        # Deleting model 'Rack'
        db.delete_table('cluster_rack')

        # Deleting model 'Country'
        db.delete_table('cluster_country')

        # Deleting model 'Address'
        db.delete_table('cluster_address')

        # Deleting model 'Room'
        db.delete_table('cluster_room')

        # Deleting model 'Company'
        db.delete_table('cluster_company')

        # Removing M2M table for field addresses on 'Company'
        db.delete_table('cluster_company_addresses')

        # Deleting model 'Connection'
        db.delete_table('cluster_connection')

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
            'Meta': {'ordering': "('postalcode',)", 'unique_together': "(('address', 'city'),)", 'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'addresses'", 'null': 'True', 'to': "orm['cluster.Country']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.cluster': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Cluster'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.company': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Company'},
            'addresses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'_companies'", 'symmetrical': 'False', 'to': "orm['cluster.Address']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'cluster.connection': {
            'Meta': {'ordering': "('company', 'address')", 'unique_together': "(('company', 'name'),)", 'object_name': 'Connection'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'connections'", 'null': 'True', 'to': "orm['cluster.Address']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'companies'", 'to': "orm['cluster.Company']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'country_code': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.hardwaremodel': {
            'Meta': {'ordering': "('vendor', 'name')", 'object_name': 'HardwareModel'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'expansions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rackspace': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'model specifications'", 'to': "orm['cluster.Company']"}),
            'vendorcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'cluster.hardwareunit': {
            'Meta': {'ordering': "('rack__label', 'first_slot')", 'unique_together': "(('rack', 'first_slot'),)", 'object_name': 'HardwareUnit'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardware'", 'to': "orm['cluster.Cluster']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'first_slot': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'symmetrical': 'False', 'through': "orm['cluster.Interface']", 'to': "orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owns'", 'null': 'True', 'to': "orm['cluster.Connection']"}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': "orm['cluster.Rack']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'hardware'", 'symmetrical': 'False', 'to': "orm['cluster.Role']"}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sold'", 'null': 'True', 'to': "orm['cluster.Connection']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'specifications': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hardware'", 'null': 'True', 'to': "orm['cluster.HardwareModel']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'warranty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'hardware'", 'null': 'True', 'to': "orm['cluster.WarrantyContract']"}),
            'warranty_tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'cluster.interface': {
            'Meta': {'ordering': "('host__cluster__name', 'host__rack__label', 'host__first_slot')", 'unique_together': "(('network', 'hwaddress'),)", 'object_name': 'Interface'},
            'aliases': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.HardwareUnit']"}),
            'hwaddress': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iftype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.InterfaceType']"}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['cluster.Network']"}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.interfacetype': {
            'Meta': {'ordering': "('label',)", 'object_name': 'InterfaceType'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'interfaces'", 'null': 'True', 'to': "orm['cluster.Company']"})
        },
        'cluster.network': {
            'Meta': {'ordering': "('name', 'domain')", 'object_name': 'Network'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gateway': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'hostnames': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'netaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'netmask': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'vlan': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        'cluster.rack': {
            'Meta': {'ordering': "('label',)", 'unique_together': "(('room', 'label'),)", 'object_name': 'Rack'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'racks'", 'to': "orm['cluster.Room']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.role': {
            'Meta': {'ordering': "('label',)", 'object_name': 'Role'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.room': {
            'Meta': {'ordering': "('address__postalcode', 'floor')", 'unique_together': "(('address', 'floor', 'label'),)", 'object_name': 'Room'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rooms'", 'to': "orm['cluster.Address']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.telephonenumber': {
            'Meta': {'ordering': "('connection',)", 'object_name': 'Telephonenumber'},
            'areacode': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'connection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': "orm['cluster.Connection']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'telephone_numbers'", 'to': "orm['cluster.Country']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'subscriber_number': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'cluster.warrantycontract': {
            'Meta': {'ordering': "('label',)", 'object_name': 'WarrantyContract'},
            'annual_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'contract_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'warranty_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contracts'", 'null': 'True', 'to': "orm['cluster.WarrantyType']"})
        },
        'cluster.warrantytype': {
            'Meta': {'ordering': "('contact__company__name', 'label')", 'object_name': 'WarrantyType'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warranty types'", 'to': "orm['cluster.Connection']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['cluster']