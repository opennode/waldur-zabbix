# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0006_extend_items'),
    ]

    operations = [
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlaHistoryEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('state', models.CharField(max_length=1, choices=[(b'U', b'DOWN'), (b'D', b'UP')])),
                ('history', models.ForeignKey(related_name='events', to='nodeconductor_zabbix.SlaHistory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='slahistory',
            unique_together=set([('host', 'period')]),
        ),
        migrations.AddField(
            model_name='host',
            name='good_sla',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='host',
            name='service_id',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='host',
            name='trigger_id',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='service_project_link',
            field=models.ForeignKey(related_name='hosts', on_delete=django.db.models.deletion.PROTECT, to='nodeconductor_zabbix.ZabbixServiceProjectLink'),
            preserve_default=True,
        ),
    ]
