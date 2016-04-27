# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0012_users_and_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='error',
            field=models.CharField(help_text='Error text if Zabbix agent is unavailable.', max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='host',
            name='status',
            field=models.CharField(default='0', max_length=30, choices=[('0', 'monitored'), ('1', 'unmonitored')]),
        ),
    ]
