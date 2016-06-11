# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0009_itservices_as_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zabbixserviceprojectlink',
            name='error_message',
        ),
        migrations.RemoveField(
            model_name='zabbixserviceprojectlink',
            name='state',
        ),
    ]
