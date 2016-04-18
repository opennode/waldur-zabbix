# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


def migrate_state_field(apps, schema_editor):
    Host = apps.get_model('nodeconductor_zabbix', 'Host')
    ITService = apps.get_model('nodeconductor_zabbix', 'ITService')

    migrate_state(Host)
    migrate_state(ITService)


def migrate_state(model):
    from nodeconductor.structure.models import OldStateResourceMixin
    from nodeconductor.core.models import StateMixin

    states_map = {
        OldStateResourceMixin.States.PROVISIONING_SCHEDULED: StateMixin.States.CREATION_SCHEDULED,
        OldStateResourceMixin.States.PROVISIONING: StateMixin.States.CREATING,

        OldStateResourceMixin.States.ONLINE: StateMixin.States.OK,
        OldStateResourceMixin.States.OFFLINE: StateMixin.States.OK,

        OldStateResourceMixin.States.STARTING_SCHEDULED: StateMixin.States.UPDATE_SCHEDULED,
        OldStateResourceMixin.States.STARTING: StateMixin.States.UPDATING,

        OldStateResourceMixin.States.STOPPING_SCHEDULED: StateMixin.States.UPDATE_SCHEDULED,
        OldStateResourceMixin.States.STOPPING: StateMixin.States.UPDATING,

        OldStateResourceMixin.States.ERRED: StateMixin.States.ERRED,

        OldStateResourceMixin.States.DELETION_SCHEDULED: StateMixin.States.DELETION_SCHEDULED,
        OldStateResourceMixin.States.DELETING: StateMixin.States.DELETING,

        OldStateResourceMixin.States.RESIZING_SCHEDULED: StateMixin.States.UPDATE_SCHEDULED,
        OldStateResourceMixin.States.RESIZING: StateMixin.States.UPDATING,

        OldStateResourceMixin.States.RESTARTING_SCHEDULED: StateMixin.States.UPDATE_SCHEDULED,
        OldStateResourceMixin.States.RESTARTING: StateMixin.States.UPDATING,
    }

    for instance in model.objects.all():
        instance.state = states_map[instance.state]
        instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('nodeconductor_zabbix', '0010_remove_spl_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='state',
            field=django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')]),
        ),
        migrations.AlterField(
            model_name='itservice',
            name='state',
            field=django_fsm.FSMIntegerField(default=5, choices=[(5, 'Creation Scheduled'), (6, 'Creating'), (1, 'Update Scheduled'), (2, 'Updating'), (7, 'Deletion Scheduled'), (8, 'Deleting'), (3, 'OK'), (4, 'Erred')]),
        ),

        migrations.RunPython(migrate_state_field),
    ]
