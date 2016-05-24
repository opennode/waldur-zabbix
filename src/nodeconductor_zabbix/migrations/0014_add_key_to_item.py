# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0013_host_status_and_error'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='key',
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default='item', max_length=255),
            preserve_default=False,
        ),
    ]
