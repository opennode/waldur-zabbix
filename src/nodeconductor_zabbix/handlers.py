import logging

from nodeconductor.structure.models import Resource

from .models import Host


logger = logging.getLogger(__name__)


def update_hosts_visible_name_on_scope_name_change(sender, instance, **kwargs):
    """ Change host visible name if visible_name of hosts scope changed """
    for host in Host.objects.filter(scope=instance):
        backend = host.get_backend()
        backend.update_visible_name(host)


def delete_hosts_on_scope_deletion(sender, instance, name, source, target, **kwargs):
    if target == Resource.States.DELETING:
        for host in Host.objects.filter(scope=instance):
            if host.backend_id:
                backend = host.get_backend()
                backend.destroy(host)
            else:
                host.delete()
