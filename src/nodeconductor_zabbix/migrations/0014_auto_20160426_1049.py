# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0013_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(default='1', max_length=30, choices=[('1', 'default'), ('2', 'admin'), ('3', 'superadmin')]),
        ),
    ]
