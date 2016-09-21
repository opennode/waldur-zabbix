# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0014_add_key_to_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='parents',
            field=models.ManyToManyField(related_name='children', to='nodeconductor_zabbix.Template'),
        ),
    ]
