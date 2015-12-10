# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('nodeconductor_zabbix', '0003_resource_error_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', blank=True),
            preserve_default=True,
        ),
    ]
