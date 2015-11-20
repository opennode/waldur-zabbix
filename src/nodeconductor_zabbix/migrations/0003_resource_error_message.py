# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0002_add_error_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='error_message',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
