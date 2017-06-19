# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_rename_hardwareunit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ('rack__label', 'first_slot'), 'verbose_name_plural': 'equipment'},
        ),
        migrations.AlterField(
            model_name='cluster',
            name='machinenames',
            field=models.CharField(blank=True, max_length=255, null=True, help_text=b"stringformat of machine names in the cluster, example: 'r{rack}n{first_slot}", validators=[django.core.validators.RegexValidator(re.compile(b'^([a-z0-9\\{]{1})([a-z0-9\\-\\_\\{\\}]{1,61})([a-z0-9\\}]{1})$'), b'Enter a valid machinenames stringformat. Example: r{rack}n{first_slot}. Valid characters: [0-9], [a-z], "{", "}" and "-"', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='interface',
            name='hwaddress',
            field=models.CharField(validators=[django.core.validators.RegexValidator(re.compile(b'([A-Fa-f\\d]{2}[:-]?){5}[A-Fa-f\\d]{2}'), b'Enter a valid MAC address. Example: "cc:cc:cc:cc:cc:cc". Valid characters: [a-f], [A-F], [0-9] and ":"', b'invalid')], max_length=17, blank=True, help_text=b"6 Octets, optionally delimited by a space ' ', a hyphen '-', or a colon ':'.", null=True, verbose_name=b'hardware address'),
        ),
        migrations.AlterField(
            model_name='interface',
            name='label',
            field=models.CharField(help_text=b'Automagically generated if kept empty', max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^([0-9a-z]{1,2})$|^([a-z0-9]{1})([a-z0-9\\-]{1,61})([a-z0-9]{1})$'), b'Enter a valid hostname. Example: "myhostname-rack2node3". Valid characters: [a-z], [0-9] and "-"', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='network',
            name='domain',
            field=models.CharField(help_text=b'example: irc.sara.nl', max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^(^(?:[a-z0-9]{1}[a-z0-9\\-]{1,61}[a-z0-9]{1}\\.?)+(?:[a-z]{2,})$)'), b'Enter a valid domain. Example: admin1.my-domain.com. Valid characters: [a-z], [0-9], "." and "-"', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='network',
            name='hostnames',
            field=models.CharField(help_text=b"stringformat of hostnames in the network, example: 'ib-{machine}", max_length=255, validators=[django.core.validators.RegexValidator(re.compile(b'^([0-9a-z]{1,2})$|^([a-z0-9\\{]{1})([a-z0-9\\-\\{\\}]{1,61})([a-z0-9\\}]{1})$'), b'Enter a valid hostnames stringformat. Example: ib-{machine}. Valid characters: [a-z], [0-9], "{", "}" and "-"', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='network',
            name='name',
            field=models.CharField(help_text=b'example: infiniband', max_length=255),
        ),
    ]
