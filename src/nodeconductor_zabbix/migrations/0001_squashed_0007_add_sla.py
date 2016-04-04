# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import nodeconductor.core.models
import django_fsm
import jsonfield.fields
import django.db.models.deletion
import django.utils.timezone
import nodeconductor.logging.loggers
import uuidfield.fields
import taggit.managers
import model_utils.fields
import nodeconductor.core.validators


class Migration(migrations.Migration):

    replaces = [('nodeconductor_zabbix', '0001_initial'), ('nodeconductor_zabbix', '0002_add_error_message'), ('nodeconductor_zabbix', '0003_resource_error_message'), ('nodeconductor_zabbix', '0004_host_tags'), ('nodeconductor_zabbix', '0005_templates_and_items'), ('nodeconductor_zabbix', '0006_extend_items'), ('nodeconductor_zabbix', '0007_add_sla')]

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0001_initial'),
        ('structure', '0025_add_zabbix_to_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZabbixService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('settings', models.ForeignKey(to='structure.ServiceSettings')),
                ('customer', models.ForeignKey(to='structure.Customer')),
                ('available_for_all', models.BooleanField(default=False, help_text='Service will be automatically added to all customers projects if it is available for all')),
            ],
            options={
                'abstract': False,
            },
            bases=(nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ZabbixServiceProjectLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', django_fsm.FSMIntegerField(default=5, choices=[(0, 'New'), (5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Sync Scheduled'), (2, 'Syncing'), (3, 'In Sync'), (4, 'Erred')])),
                ('project', models.ForeignKey(to='structure.Project')),
                ('service', models.ForeignKey(to='nodeconductor_zabbix.ZabbixService')),
                ('error_message', models.TextField(blank=True)),
            ],
            bases=(nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='zabbixservice',
            unique_together=set([('customer', 'settings')]),
        ),
        migrations.AlterUniqueTogether(
            name='zabbixserviceprojectlink',
            unique_together=set([('service', 'project')]),
        ),
        migrations.AddField(
            model_name='zabbixservice',
            name='projects',
            field=models.ManyToManyField(related_name='zabbix_services', through='nodeconductor_zabbix.ZabbixServiceProjectLink', to=b'structure.Project'),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('backend_id', models.CharField(max_length=255, db_index=True)),
                ('settings', models.ForeignKey(related_name='+', to='structure.ServiceSettings')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('settings', 'backend_id')]),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('description', models.CharField(max_length=500, verbose_name='description', blank=True)),
                ('name', models.CharField(max_length=64, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('backend_id', models.CharField(max_length=255, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('state', django_fsm.FSMIntegerField(default=1, help_text='WARNING! Should not be changed manually unless you really know what you are doing.', choices=[(1, 'Provisioning Scheduled'), (2, 'Provisioning'), (3, 'Online'), (4, 'Offline'), (5, 'Starting Scheduled'), (6, 'Starting'), (7, 'Stopping Scheduled'), (8, 'Stopping'), (9, 'Erred'), (10, 'Deletion Scheduled'), (11, 'Deleting'), (13, 'Resizing Scheduled'), (14, 'Resizing'), (15, 'Restarting Scheduled'), (16, 'Restarting')])),
                ('visible_name', models.CharField(max_length=64, verbose_name='visible name')),
                ('interface_parameters', jsonfield.fields.JSONField(blank=True)),
                ('host_group_name', models.CharField(max_length=64, verbose_name='host group name', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('service_project_link', models.ForeignKey(related_name='hosts', on_delete=django.db.models.deletion.PROTECT, to='nodeconductor_zabbix.ZabbixServiceProjectLink')),
                ('error_message', models.TextField(blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('templates', models.ManyToManyField(related_name='hosts', to=b'nodeconductor_zabbix.Template')),
                ('agreed_sla', models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True)),
                ('service_id', models.CharField(max_length=255, blank=True)),
                ('trigger_id', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(nodeconductor.core.models.SerializableAbstractMixin, nodeconductor.core.models.DescendantMixin, nodeconductor.logging.loggers.LoggableMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('template', models.ForeignKey(related_name='items', to='nodeconductor_zabbix.Template')),
                ('backend_id', models.CharField(max_length=64)),
                ('delay', models.IntegerField()),
                ('history', models.IntegerField()),
                ('units', models.CharField(max_length=255)),
                ('value_type', models.IntegerField(choices=[(0, b'Numeric (float)'), (1, b'Character'), (2, b'Log'), (3, b'Numeric (unsigned)'), (4, b'Text')])),
            ],
        ),
        migrations.CreateModel(
            name='SlaHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.CharField(max_length=10)),
                ('value', models.DecimalField(null=True, max_digits=11, decimal_places=4, blank=True)),
                ('host', models.ForeignKey(to='nodeconductor_zabbix.Host')),
            ],
            options={
                'verbose_name': 'SLA history',
                'verbose_name_plural': 'SLA histories',
            },
        ),
        migrations.CreateModel(
            name='SlaHistoryEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('state', models.CharField(max_length=1, choices=[(b'U', b'DOWN'), (b'D', b'UP')])),
                ('history', models.ForeignKey(related_name='events', to='nodeconductor_zabbix.SlaHistory')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='slahistory',
            unique_together=set([('host', 'period')]),
        ),
    ]
