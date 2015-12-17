# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0005_templates_and_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='delay',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='history',
            field=models.IntegerField(default=90),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='units',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='value_type',
            field=models.IntegerField(default=0, choices=[(0, b'Numeric (float)'), (1, b'Character'), (2, b'Log'), (3, b'Numeric (unsigned)'), (4, b'Text')]),
            preserve_default=False,
        ),
    ]
