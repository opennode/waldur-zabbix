# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0028_servicesettings_service_type2'),
        ('nodeconductor_zabbix', '0004_host_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('backend_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('backend_id', models.CharField(max_length=255, db_index=True)),
                ('settings', models.ForeignKey(related_name='+', to='structure.ServiceSettings')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('settings', 'backend_id')]),
        ),
        migrations.AddField(
            model_name='item',
            name='template',
            field=models.ForeignKey(related_name='items', to='nodeconductor_zabbix.Template'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='host',
            name='templates',
            field=models.ManyToManyField(related_name='hosts', to='nodeconductor_zabbix.Template'),
            preserve_default=True,
        ),
    ]
