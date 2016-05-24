# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuidfield.fields
import django_fsm
import nodeconductor.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0034_change_service_settings_state_field'),
        ('nodeconductor_zabbix', '0011_migrate_state_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('state', django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')])),
                ('backend_id', models.CharField(max_length=255, db_index=True)),
                ('alias', models.CharField(max_length=150)),
                ('surname', models.CharField(max_length=150)),
                ('type', models.CharField(default='1', max_length=30, choices=[('1', 'default'), ('2', 'admin'), ('3', 'superadmin')])),
                ('password', models.CharField(max_length=150, blank=True)),
                ('phone', models.CharField(max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
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
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='users', to='nodeconductor_zabbix.UserGroup'),
        ),
        migrations.AddField(
            model_name='user',
            name='settings',
            field=models.ForeignKey(related_name='+', to='structure.ServiceSettings'),
        ),
        migrations.AlterUniqueTogether(
            name='usergroup',
            unique_together=set([('settings', 'backend_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('alias', 'settings')]),
        ),
    ]
