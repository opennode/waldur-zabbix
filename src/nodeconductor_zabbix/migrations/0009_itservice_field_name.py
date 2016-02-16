# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0008_add_itservice_trigger'),
    ]

    operations = [
        migrations.AddField(
            model_name='itservice',
            name='field_name',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
