# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import taggit.managers
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('nodeconductor_zabbix', '0008_add_itservice_trigger'),
    ]

    operations = [
        migrations.AddField(
            model_name='itservice',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='description',
            field=models.CharField(max_length=500, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='error_message',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='is_main',
            field=models.BooleanField(default=True, help_text='Main IT service SLA will be added to hosts resource as monitoring item.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='service_project_link',
            field=models.ForeignKey(related_name='itservices', on_delete=django.db.models.deletion.PROTECT, default=1, to='nodeconductor_zabbix.ZabbixServiceProjectLink'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itservice',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='state',
            field=django_fsm.FSMIntegerField(default=1, help_text='WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itservice',
            name='backend_id',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='itservice',
            name='host',
            field=models.ForeignKey(related_name='itservices', blank=True, to='nodeconductor_zabbix.Host', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='itservice',
            unique_together=set([('host', 'is_main')]),
        ),
        migrations.RemoveField(
            model_name='itservice',
            name='settings',
        ),
    ]
