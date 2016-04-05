# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields

import nodeconductor.core.models
import nodeconductor.core.validators
import nodeconductor.logging.loggers


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
                ('name', models.CharField(max_length=150, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('backend_id', models.CharField(max_length=255, db_index=True)),
                ('settings', models.ForeignKey(related_name='+', to='structure.ServiceSettings')),
                ('agreed_sla', models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True)),
                ('algorithm', models.PositiveSmallIntegerField(default=0, choices=[(0, b'do not calculate'), (1, b'problem, if at least one child has a problem'), (2, b'problem, if all children have problems')])),
                ('sort_order', models.PositiveSmallIntegerField(default=1)),
                ('host', models.ForeignKey(on_delete=models.deletion.PROTECT, blank=True, to='nodeconductor_zabbix.Host', null=True)),
                ('backend_trigger_id', models.CharField(max_length=64, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='itservice',
            unique_together=set([('settings', 'backend_id')]),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name', validators=[nodeconductor.core.validators.validate_name])),
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
            field=models.ForeignKey(blank=True, to='nodeconductor_zabbix.Trigger', null=True),
            preserve_default=False,
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
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slahistory',
            name='itservice',
            field=models.ForeignKey(to='nodeconductor_zabbix.ITService'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='slahistory',
            unique_together=set([('itservice', 'period')]),
        ),
        migrations.RemoveField(
            model_name='slahistory',
            name='host',
        ),
    ]
