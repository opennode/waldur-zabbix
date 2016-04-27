import logging

from nodeconductor.structure.models import Resource

from . import executors
from .models import Host


logger = logging.getLogger(__name__)


def update_hosts_visible_name_on_scope_name_change(sender, instance, **kwargs):
    """ Change host visible name if visible_name of hosts scope changed """
    for host in Host.objects.filter(scope=instance):
        host.visible_name = host.get_visible_name_from_scope(host.scope)
        host.save()
        executors.HostUpdateExecutor.execute(host, updated_fields=['visible_name'])


def delete_hosts_on_scope_deletion(sender, instance, name, source, target, **kwargs):
    if target != Resource.States.DELETING:
        return
    for host in Host.objects.filter(scope=instance):
        if host.state == Host.States.OK:
            executors.HostDeleteExecutor.execute(host)
        elif host.state == Host.States.ERRED:
            executors.HostDeleteExecutor.execute(host, force=True)
        else:
            logger.exception(
                'Instance %s host was in state %s on instance deletion.', instance, host.human_readable_state)
            host.set_erred()
            host.save()
            executors.HostDeleteExecutor.execute(host, force=True)
