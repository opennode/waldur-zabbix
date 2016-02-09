# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_fsm
import model_utils.fields
import taggit.managers
import uuidfield.fields

import nodeconductor.core.models
import nodeconductor.core.validators
import nodeconductor.logging.log


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('structure', '0032_make_options_optional'),
        ('nodeconductor_zabbix', '0007_add_sla'),
    ]

    operations = [
        migrations.CreateModel(
            name='ITService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('description', models.CharField(max_length=500, verbose_name='description', blank=True)),
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('backend_id', models.CharField(max_length=255, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('state', django_fsm.FSMIntegerField(default=1, help_text='WARNING! Should not be changed manually unless you really know what you are doing.', max_length=1, choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
                ('agreed_sla', models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True)),
                ('host', models.ForeignKey(to='nodeconductor_zabbix.Host', on_delete=django.db.models.deletion.PROTECT)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.log.LoggableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('backend_id', models.CharField(max_length=255, db_index=True)),
                ('settings', models.ForeignKey(related_name='+', to='structure.ServiceSettings')),
                ('template', models.ForeignKey(related_name='triggers', to='nodeconductor_zabbix.Template')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='trigger',
            unique_together=set([('settings', 'backend_id')]),
        ),
        migrations.AddField(
            model_name='itservice',
            name='trigger',
            field=models.ForeignKey(to='nodeconductor_zabbix.Trigger'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='host',
            name='agreed_sla',
        ),
        migrations.RemoveField(
            model_name='host',
            name='service_id',
        ),
        migrations.RemoveField(
            model_name='host',
            name='trigger_id',
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name', validators=[nodeconductor.core.validators.validate_name]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itservice',
            name='service_project_link',
            field=models.ForeignKey(related_name='itservice', on_delete=django.db.models.deletion.PROTECT, to='nodeconductor_zabbix.ZabbixServiceProjectLink'),
            preserve_default=False,
        )
    ]
