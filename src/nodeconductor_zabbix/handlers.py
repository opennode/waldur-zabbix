import logging

from nodeconductor.structure.models import Resource

from . import executors
from .models import Host


logger = logging.getLogger(__name__)


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
