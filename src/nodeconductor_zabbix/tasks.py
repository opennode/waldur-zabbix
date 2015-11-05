import logging

from celery import shared_task

from nodeconductor.core.tasks import transition
from .models import Host


logger = logging.getLogger(__name__)


@shared_task(name='nodeconductor.zabbix.provision')
def provision(host_uuid):
    provision_host.apply_async(
        args=(host_uuid,),
        link=set_online.si(host_uuid),
        link_error=set_erred.si(host_uuid)
    )


@shared_task(name='nodeconductor.zabbix.destroy')
def destroy(host_uuid):
    destroy_host.apply_async(
        args=(host_uuid,),
        link=delete.si(host_uuid),
        link_error=set_erred.si(host_uuid),
    )


@shared_task
@transition(Host, 'begin_provisioning')
def provision_host(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.provision_host(host)


@shared_task
@transition(Host, 'begin_deleting')
def destroy_host(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.destroy_host(host)


@shared_task
@transition(Host, 'set_online')
def set_online(host_uuid, transition_entity=None):
    pass


@shared_task
@transition(Host, 'set_offline')
def set_offline(host_uuid, transition_entity=None):
    pass


@shared_task
@transition(Host, 'schedule_deletion')
def schedule_deletion(host_uuid, transition_entity=None):
    pass


@shared_task
@transition(Host, 'set_erred')
def set_erred(host_uuid, transition_entity=None):
    pass


@shared_task
def delete(host_uuid):
    Host.objects.get(uuid=host_uuid).delete()
