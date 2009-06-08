
from south.db import db
from django.db import models
from sara_cmt.cluster.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'InterfaceType'
        db.create_table('cluster_interfacetype', (
            ('id', models.AutoField(primary_key=True)),
            ('label', models.CharField(max_length=30)),
            ('vendor', models.ForeignKey(orm.Company, related_name='interfaces', null=True, blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['InterfaceType'])
        
        # Adding model 'HardwareSpecifications'
        db.create_table('cluster_hardwarespecifications', (
            ('id', models.AutoField(primary_key=True)),
            ('vendor', models.ForeignKey(orm.Company, related_name='model specifications')),
            ('name', models.CharField(unique=True, max_length=30)),
            ('system_id', models.CharField(max_length=30, blank=True)),
            ('slots_size', models.PositiveIntegerField()),
            ('slots_capacity', models.PositiveIntegerField(default=0)),
        ))
        db.send_create_signal('cluster', ['HardwareSpecifications'])
        
        # Adding model 'Cluster'
        db.create_table('cluster_cluster', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(unique=True, max_length=30)),
            ('note', models.TextField(blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Cluster'])
        
        # Adding model 'Company'
        db.create_table('cluster_company', (
            ('location_ptr', models.OneToOneField(orm['cluster.Location'])),
            ('name', models.CharField(max_length=30)),
            ('website', models.URLField(verify_exists=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Company'])
        
        # Adding model 'Contact'
        db.create_table('cluster_contact', (
            ('location_ptr', models.OneToOneField(orm['cluster.Location'])),
            ('employer', models.ForeignKey(orm.Company, related_name='employees')),
            ('department', models.ForeignKey(orm.Department, related_name='employees', null=True, blank=True)),
            ('position', models.ForeignKey(orm.Position, related_name='contacts')),
            ('added_on', models.DateField(default=date.today, editable=False)),
            ('active', models.BooleanField(default=True, editable=True)),
            ('note', models.TextField(default='', blank=True)),
            ('firstname', models.CharField(max_length=30)),
            ('lastname', models.CharField(max_length=30)),
            ('email', models.EmailField()),
            ('phone', models.CharField(max_length=17)),
            ('cellphone', models.CharField(max_length=17)),
            ('fax', models.CharField(max_length=17, blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Contact'])
        
        # Adding model 'Role'
        db.create_table('cluster_role', (
            ('id', models.AutoField(primary_key=True)),
            ('label', models.CharField(unique=True, max_length=30)),
            ('note', models.TextField(blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Role'])
        
        # Adding model 'Interface'
        db.create_table('cluster_interface', (
            ('id', models.AutoField(primary_key=True)),
            ('network', models.ForeignKey(orm.Network, related_name='interfaces')),
            ('hardware', models.ForeignKey(orm.HardwareUnit, related_name='interfaces')),
            ('type', models.ForeignKey(orm.InterfaceType, related_name='interfaces')),
            ('name', models.CharField(max_length=30, blank=True)),
            ('hwaddress', MACAddressField(null=True, blank=True)),
            ('ip', models.IPAddressField(null=True, editable=False, blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Interface'])
        
        # Adding model 'HardwareUnit'
        db.create_table('cluster_hardwareunit', (
            ('id', models.AutoField(primary_key=True)),
            ('cluster', models.ForeignKey(orm.Cluster, related_name='hardware')),
            ('role', models.ForeignKey(orm.Role, related_name='hardware')),
            ('specifications', models.ForeignKey(orm.HardwareSpecifications, related_name='hardware', null=True, blank=True)),
            ('warranty', models.ForeignKey(orm.Warranty, related_name='hardware', null=True, blank=True)),
            ('rack', models.ForeignKey(orm.Rack, related_name='contents')),
            ('service_tag', models.CharField(unique=True, max_length=30, blank=True)),
            ('serialnumber', models.CharField(unique=True, max_length=30, blank=True)),
            ('first_slot', models.PositiveIntegerField()),
            ('hostname', models.CharField(max_length=30, blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['HardwareUnit'])
        
        # Adding model 'Network'
        db.create_table('cluster_network', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=30)),
            ('netaddress', models.IPAddressField()),
            ('netmask', models.IPAddressField()),
            ('domain', models.CharField(max_length=30)),
            ('prefix', models.CharField(max_length=10, blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Network'])
        
        # Adding model 'Location'
        db.create_table('cluster_location', (
            ('id', models.AutoField(primary_key=True)),
            ('address1', models.CharField(max_length=30)),
            ('address2', models.CharField(max_length=30, blank=True)),
            ('postalcode', models.CharField(max_length=9, blank=True)),
            ('city', models.CharField(max_length=30)),
            ('country', models.CharField(max_length=30, blank=True)),
            ('room', models.CharField(max_length=30, blank=True)),
        ))
        db.send_create_signal('cluster', ['Location'])
        
        # Adding model 'Department'
        db.create_table('cluster_department', (
            ('id', models.AutoField(primary_key=True)),
            ('label', models.CharField(max_length=50)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Department'])
        
        # Adding model 'Rack'
        db.create_table('cluster_rack', (
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm.Site, related_name='racks')),
            ('label', models.SlugField(max_length=30)),
            ('note', models.TextField(default='', blank=True)),
            ('capacity', models.PositiveIntegerField()),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Rack'])
        
        # Adding model 'Site'
        db.create_table('cluster_site', (
            ('location_ptr', models.OneToOneField(orm['cluster.Location'])),
            ('name', models.SlugField(unique=True, max_length=30, editable=False)),
            ('note', models.TextField(blank=True)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Site'])
        
        # Adding model 'Warranty'
        db.create_table('cluster_warranty', (
            ('id', models.AutoField(primary_key=True)),
            ('label', models.CharField(unique=True, max_length=30)),
            ('date_from', models.DateField()),
            ('months', models.PositiveIntegerField()),
            ('date_to', models.DateField(editable=False)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Warranty'])
        
        # Adding model 'Position'
        db.create_table('cluster_position', (
            ('id', models.AutoField(primary_key=True)),
            ('label', models.CharField(max_length=30)),
            ('tags', TagField()),
        ))
        db.send_create_signal('cluster', ['Position'])
        
        # Creating unique_together for [rack, first_slot] on HardwareUnit.
        db.create_unique('cluster_hardwareunit', ['rack_id', 'first_slot'])
        
        # Creating unique_together for [firstname, lastname] on Contact.
        db.create_unique('cluster_contact', ['firstname', 'lastname'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'InterfaceType'
        db.delete_table('cluster_interfacetype')
        
        # Deleting model 'HardwareSpecifications'
        db.delete_table('cluster_hardwarespecifications')
        
        # Deleting model 'Cluster'
        db.delete_table('cluster_cluster')
        
        # Deleting model 'Company'
        db.delete_table('cluster_company')
        
        # Deleting model 'Contact'
        db.delete_table('cluster_contact')
        
        # Deleting model 'Role'
        db.delete_table('cluster_role')
        
        # Deleting model 'Interface'
        db.delete_table('cluster_interface')
        
        # Deleting model 'HardwareUnit'
        db.delete_table('cluster_hardwareunit')
        
        # Deleting model 'Network'
        db.delete_table('cluster_network')
        
        # Deleting model 'Location'
        db.delete_table('cluster_location')
        
        # Deleting model 'Department'
        db.delete_table('cluster_department')
        
        # Deleting model 'Rack'
        db.delete_table('cluster_rack')
        
        # Deleting model 'Site'
        db.delete_table('cluster_site')
        
        # Deleting model 'Warranty'
        db.delete_table('cluster_warranty')
        
        # Deleting model 'Position'
        db.delete_table('cluster_position')
        
        # Deleting unique_together for [rack, first_slot] on HardwareUnit.
        db.delete_unique('cluster_hardwareunit', ['rack_id', 'first_slot'])
        
        # Deleting unique_together for [firstname, lastname] on Contact.
        db.delete_unique('cluster_contact', ['firstname', 'lastname'])
        
    
    
    models = {
        'cluster.interfacetype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '30'}),
            'tags': ('TagField', [], {}),
            'vendor': ('models.ForeignKey', ["orm['cluster.Company']"], {'related_name': "'interfaces'", 'null': 'True', 'blank': 'True'})
        },
        'cluster.hardwarespecifications': {
            'Meta': {'ordering': "('vendor','name')"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slots_capacity': ('models.PositiveIntegerField', [], {'default': '0'}),
            'slots_size': ('models.PositiveIntegerField', [], {}),
            'system_id': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'vendor': ('models.ForeignKey', ["orm['cluster.Company']"], {'related_name': "'model specifications'"})
        },
        'cluster.cluster': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'note': ('models.TextField', [], {'blank': 'True'}),
            'tags': ('TagField', [], {})
        },
        'cluster.company': {
            'Meta': {'_bases': ['sara_cmt.cluster.models.Location']},
            'location_ptr': ('models.OneToOneField', ["orm['cluster.Location']"], {}),
            'name': ('models.CharField', [], {'max_length': '30'}),
            'tags': ('TagField', [], {}),
            'website': ('models.URLField', [], {'verify_exists': 'True'})
        },
        'cluster.contact': {
            'Meta': {'ordering': "('lastname','firstname')", 'unique_together': "('firstname','lastname')", '_bases': ['sara_cmt.cluster.models.Location']},
            'active': ('models.BooleanField', [], {'default': 'True', 'editable': 'True'}),
            'added_on': ('models.DateField', [], {'default': 'date.today', 'editable': 'False'}),
            'cellphone': ('models.CharField', [], {'max_length': '17'}),
            'department': ('models.ForeignKey', ["orm['cluster.Department']"], {'related_name': "'employees'", 'null': 'True', 'blank': 'True'}),
            'email': ('models.EmailField', [], {}),
            'employer': ('models.ForeignKey', ["orm['cluster.Company']"], {'related_name': "'employees'"}),
            'fax': ('models.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'firstname': ('models.CharField', [], {'max_length': '30'}),
            'lastname': ('models.CharField', [], {'max_length': '30'}),
            'location_ptr': ('models.OneToOneField', ["orm['cluster.Location']"], {}),
            'note': ('models.TextField', [], {'default': "''", 'blank': 'True'}),
            'phone': ('models.CharField', [], {'max_length': '17'}),
            'position': ('models.ForeignKey', ["orm['cluster.Position']"], {'related_name': "'contacts'"}),
            'tags': ('TagField', [], {})
        },
        'cluster.role': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'note': ('models.TextField', [], {'blank': 'True'}),
            'tags': ('TagField', [], {})
        },
        'cluster.warranty': {
            'date_from': ('models.DateField', [], {}),
            'date_to': ('models.DateField', [], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'months': ('models.PositiveIntegerField', [], {}),
            'tags': ('TagField', [], {})
        },
        'cluster.hardwareunit': {
            'Meta': {'ordering': "['rack__label','first_slot']", 'unique_together': "[('rack','first_slot')]"},
            'cluster': ('models.ForeignKey', ["orm['cluster.Cluster']"], {'related_name': "'hardware'"}),
            'first_slot': ('models.PositiveIntegerField', [], {}),
            'hostname': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'networks': ('models.ManyToManyField', ["orm['cluster.Network']"], {'through': "'Interface'"}),
            'rack': ('models.ForeignKey', ["orm['cluster.Rack']"], {'related_name': "'contents'"}),
            'role': ('models.ForeignKey', ["orm['cluster.Role']"], {'related_name': "'hardware'"}),
            'serialnumber': ('models.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'service_tag': ('models.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'specifications': ('models.ForeignKey', ["orm['cluster.HardwareSpecifications']"], {'related_name': "'hardware'", 'null': 'True', 'blank': 'True'}),
            'tags': ('TagField', [], {}),
            'warranty': ('models.ForeignKey', ["orm['cluster.Warranty']"], {'related_name': "'hardware'", 'null': 'True', 'blank': 'True'})
        },
        'cluster.network': {
            'domain': ('models.CharField', [], {'max_length': '30'}),
            'equipment': ('models.ManyToManyField', ["orm['cluster.HardwareUnit']"], {'through': "'Interface'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '30'}),
            'netaddress': ('models.IPAddressField', [], {}),
            'netmask': ('models.IPAddressField', [], {}),
            'prefix': ('models.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'tags': ('TagField', [], {})
        },
        'cluster.department': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '50'}),
            'tags': ('TagField', [], {})
        },
        'cluster.location': {
            'address1': ('models.CharField', [], {'max_length': '30'}),
            'address2': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'city': ('models.CharField', [], {'max_length': '30'}),
            'country': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'postalcode': ('models.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'room': ('models.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'cluster.site': {
            'Meta': {'ordering': "['country','city','address1']", '_bases': ['sara_cmt.cluster.models.Location']},
            'location_ptr': ('models.OneToOneField', ["orm['cluster.Location']"], {}),
            'name': ('models.SlugField', [], {'unique': 'True', 'max_length': '30', 'editable': 'False'}),
            'note': ('models.TextField', [], {'blank': 'True'}),
            'tags': ('TagField', [], {})
        },
        'cluster.rack': {
            'Meta': {'ordering': "('site','label',)"},
            'capacity': ('models.PositiveIntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.SlugField', [], {'max_length': '30'}),
            'note': ('models.TextField', [], {'default': "''", 'blank': 'True'}),
            'site': ('models.ForeignKey', ["orm['cluster.Site']"], {'related_name': "'racks'"}),
            'tags': ('TagField', [], {})
        },
        'cluster.interface': {
            'hardware': ('models.ForeignKey', ["orm['cluster.HardwareUnit']"], {'related_name': "'interfaces'"}),
            'hwaddress': ('MACAddressField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', [], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'network': ('models.ForeignKey', ["orm['cluster.Network']"], {'related_name': "'interfaces'"}),
            'tags': ('TagField', [], {}),
            'type': ('models.ForeignKey', ["orm['cluster.InterfaceType']"], {'related_name': "'interfaces'"})
        },
        'cluster.position': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'label': ('models.CharField', [], {'max_length': '30'}),
            'tags': ('TagField', [], {})
        }
    }
    
    complete_apps = ['cluster']
