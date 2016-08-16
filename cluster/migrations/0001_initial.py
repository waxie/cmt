# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import tagging.fields
import django_extensions.db.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('address', models.CharField(max_length=255)),
                ('postalcode', models.CharField(max_length=9, blank=True)),
                ('city', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('postalcode',),
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('machinenames', models.CharField(blank=True, max_length=255, null=True, help_text=b"stringformat                                   of machine names in the cluster, example:                                   'r{rack}n{first_slot}", validators=[django.core.validators.RegexValidator(re.compile(b'^([a-z0-9\\{]{1})([a-z0-9\\-\\_\\{\\}]{1,61})([a-z0-9\\}]{1})$'), b'Enter a valid machinenames stringformat. Example: r{rack}n{first_slot}. Valid characters: [0-9], [a-z], "{", "}" and "-"', b'invalid')])),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('website', models.URLField()),
                ('addresses', models.ManyToManyField(related_name='_companies', to='cluster.Address')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'full name')),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('address', models.ForeignKey(related_name='connections', blank=True, to='cluster.Address', null=True)),
                ('company', models.ForeignKey(related_name='companies', to='cluster.Company')),
            ],
            options={
                'ordering': ('company', 'address'),
                'verbose_name': 'contact',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('country_code', models.PositiveIntegerField(help_text=b"Example: In case of The Netherlands it's 31", unique=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='HardwareModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('vendorcode', models.CharField(help_text=b'example: CISCO7606-S', max_length=255, unique=True, null=True, blank=True)),
                ('rackspace', models.PositiveIntegerField(help_text=b'size in U for example')),
                ('expansions', models.PositiveIntegerField(default=0, help_text=b'number of expansion slots')),
                ('vendor', models.ForeignKey(related_name='hardware', to='cluster.Company')),
            ],
            options={
                'ordering': ('vendor', 'name'),
                'verbose_name': 'model',
            },
        ),
        migrations.CreateModel(
            name='HardwareUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('state', models.CharField(default=b'unknown', max_length=10, null=True, blank=True, choices=[(b'new', b'new'), (b'clean', b'clean'), (b'configured', b'configured'), (b'unknown', b'unknown'), (b'off', b'off')])),
                ('warranty_tag', models.CharField(help_text=b'Service tag', max_length=255, unique=True, null=True, blank=True)),
                ('serial_number', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('first_slot', models.PositiveIntegerField(null=True, blank=True)),
                ('label', models.CharField(max_length=255)),
                ('cluster', models.ForeignKey(related_name='hardware', to='cluster.Cluster')),
            ],
            options={
                'ordering': ('rack__label', 'first_slot'),
                'verbose_name_plural': 'hardware',
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('label', models.CharField(help_text=b'Automagically                                  generated if kept empty', max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^([0-9a-z]{1,2})$|^([a-z0-9]{1})([a-z0-9\\-]{1,61})([a-z0-9]{1})$'), b'Enter a valid hostname. Example: "myhostname-rack2node3". Valid characters: [a-z], [0-9] and "-"', b'invalid')])),
                ('aliases', models.CharField(blank=True, max_length=255, null=True, help_text=b'Cnames comma-seperated', validators=[django.core.validators.RegexValidator(re.compile(b'^[a-z\\d\\-\\.]+([,]{1}[a-z\\d\\-\\.]+)*$'), b'One or more (comma seperated, no spaces) aliases. Example: "test,test.console,alias2". Valid characters: [a-z], [0-9], "-", "." and ","', b'invalid')])),
                ('hwaddress', models.CharField(validators=[django.core.validators.RegexValidator(re.compile(b'([A-Fa-f\\d]{2}[:-]?){5}[A-Fa-f\\d]{2}'), b'Enter a valid MAC address. Example: "cc:cc:cc:cc:cc:cc". Valid characters: [a-f], [A-F], [0-9] and ":"', b'invalid')], max_length=17, blank=True, help_text=b"6 Octets, optionally delimited by                                  a space ' ', a hyphen '-', or a colon ':'.", null=True, verbose_name=b'hardware address')),
                ('ip', models.GenericIPAddressField(null=True, blank=True)),
                ('host', models.ForeignKey(related_name='interfaces', verbose_name=b'machine', to='cluster.HardwareUnit')),
            ],
            options={
                'ordering': ('host__cluster__name', 'host__rack__label', 'host__first_slot'),
            },
        ),
        migrations.CreateModel(
            name='InterfaceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('label', models.CharField(help_text=b"'DRAC 4' for example", max_length=255)),
                ('vendor', models.ForeignKey(related_name='interfaces', blank=True, to='cluster.Company', null=True)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'type of interface',
                'verbose_name_plural': 'types of interfaces',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(help_text=b'example:                                   infiniband', max_length=255)),
                ('cidr', models.CharField(help_text=b'example: 192.168.1.0/24 or fd47:e249:06b2:0385::/64', max_length=100)),
                ('gateway', models.GenericIPAddressField(help_text=b'Automagically generated if kept empty', null=True, blank=True)),
                ('domain', models.CharField(help_text=b'example:                                   irc.sara.nl', max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^(^(?:[a-z0-9]{1}[a-z0-9\\-]{1,61}[a-z0-9]{1}\\.?)+(?:[a-z]{2,})$)'), b'Enter a valid domain. Example: admin1.my-domain.com. Valid characters: [a-z], [0-9], "." and "-"', b'invalid')])),
                ('vlan', models.PositiveIntegerField(null=True, blank=True)),
                ('hostnames', models.CharField(help_text=b"stringformat                                   of hostnames in the network, example:                                   'ib-{machine}", max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^([0-9a-z]{1,2})$|^([a-z0-9\\{]{1})([a-z0-9\\-\\{\\}]{1,61})([a-z0-9\\}]{1})$'), b'Enter a valid hostnames stringformat. Example: ib-{machine}. Valid characters: [a-z], [0-9], "{", "}" and "-"', b'invalid')])),
            ],
            options={
                'ordering': ('name', 'domain'),
                'verbose_name': 'network',
                'verbose_name_plural': 'networks',
            },
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('label', models.SlugField(max_length=255)),
                ('capacity', models.PositiveIntegerField(verbose_name=b'number of slots')),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'rack',
                'verbose_name_plural': 'racks',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('label', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('floor', models.IntegerField()),
                ('label', models.CharField(max_length=255)),
                ('address', models.ForeignKey(related_name='rooms', to='cluster.Address')),
            ],
            options={
                'ordering': ('address__postalcode', 'floor'),
            },
        ),
        migrations.CreateModel(
            name='Telephonenumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('areacode', models.CharField(max_length=4)),
                ('subscriber_number', models.IntegerField(verbose_name=b'number')),
                ('number_type', models.CharField(max_length=1, choices=[(b'T', b'Telephone'), (b'C', b'Cellphone'), (b'F', b'Fax')])),
                ('connection', models.ForeignKey(related_name='telephone_numbers', to='cluster.Connection')),
                ('country', models.ForeignKey(related_name='telephone_numbers', to='cluster.Country')),
            ],
            options={
                'ordering': ('connection',),
            },
        ),
        migrations.CreateModel(
            name='WarrantyContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('contract_number', models.CharField(help_text=b'NSEN420201', max_length=255, unique=True, null=True, blank=True)),
                ('annual_cost', models.DecimalField(help_text=b'433.61', null=True, max_digits=8, decimal_places=2, blank=True)),
                ('label', models.CharField(unique=True, max_length=255)),
                ('date_from', models.DateField(verbose_name=b'valid from')),
                ('date_to', models.DateField(verbose_name=b'expires at')),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='WarrantyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('created_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('label', models.CharField(unique=True, max_length=255)),
                ('contact', models.ForeignKey(related_name='warranty', to='cluster.Connection')),
            ],
            options={
                'ordering': ('contact__company__name', 'label'),
            },
        ),
        migrations.AddField(
            model_name='warrantycontract',
            name='warranty_type',
            field=models.ForeignKey(related_name='contracts', blank=True, to='cluster.WarrantyType', null=True),
        ),
        migrations.AddField(
            model_name='rack',
            name='room',
            field=models.ForeignKey(related_name='racks', to='cluster.Room'),
        ),
        migrations.AddField(
            model_name='interface',
            name='iftype',
            field=models.ForeignKey(related_name='interfaces', verbose_name=b'type', to='cluster.InterfaceType'),
        ),
        migrations.AddField(
            model_name='interface',
            name='network',
            field=models.ForeignKey(related_name='interfaces', to='cluster.Network'),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='network',
            field=models.ManyToManyField(related_name='hardware', through='cluster.Interface', to='cluster.Network'),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='owner',
            field=models.ForeignKey(related_name='owns', blank=True, to='cluster.Connection', null=True),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='rack',
            field=models.ForeignKey(related_name='contents', to='cluster.Rack'),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='role',
            field=models.ManyToManyField(related_name='hardware', to='cluster.Role'),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='seller',
            field=models.ForeignKey(related_name='sold', blank=True, to='cluster.Connection', null=True),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='specifications',
            field=models.ForeignKey(related_name='hardware', blank=True, to='cluster.HardwareModel', null=True),
        ),
        migrations.AddField(
            model_name='hardwareunit',
            name='warranty',
            field=models.ForeignKey(related_name='hardware', blank=True, to='cluster.WarrantyContract', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(related_name='addresses', blank=True, to='cluster.Country', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together=set([('address', 'floor', 'label')]),
        ),
        migrations.AlterUniqueTogether(
            name='rack',
            unique_together=set([('room', 'label')]),
        ),
        migrations.AlterUniqueTogether(
            name='interface',
            unique_together=set([('network', 'hwaddress')]),
        ),
        migrations.AlterUniqueTogether(
            name='hardwareunit',
            unique_together=set([('rack', 'first_slot'), ('cluster', 'label')]),
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together=set([('company', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('address', 'city')]),
        ),
    ]
