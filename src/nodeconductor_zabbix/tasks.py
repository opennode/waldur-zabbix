import datetime
from decimal import Decimal
import logging

from celery import shared_task

from nodeconductor.core.tasks import save_error_message, transition
from .backend import ZabbixBackendError
from .models import Host, SlaHistory


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


@shared_task(name='nodeconductor.zabbix.update_visible_name')
def update_visible_name(host_uuid):
    host = Host.objects.get(uuid=host_uuid)
    backend = host.get_backend()
    backend.update_host_visible_name(host)


@shared_task
@transition(Host, 'begin_provisioning')
@save_error_message
def provision_host(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.provision_host(host)


@shared_task
@transition(Host, 'begin_deleting')
@save_error_message
def destroy_host(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.destroy_host(host)

    if host.service_id:
        backend.delete_service(host.service_id)


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


@shared_task
def update_sla(sla_type):
    if sla_type not in ('yearly', 'monthly'):
        logger.error('Requested unknown SLA type: %s' % sla_type)
        return

    dt = datetime.datetime.now()

    if sla_type == 'yearly':
        period = dt.year
        start_time = int(datetime.datetime.strptime('01/01/%s' % dt.year, '%d/%m/%Y').strftime("%s"))
    else:  # it's a monthly SLA update
        period = '%s-%s' % (dt.year, dt.month)
        month_start = datetime.datetime.strptime('01/%s/%s' % (dt.month, dt.year), '%d/%m/%Y')
        start_time = int(month_start.strftime("%s"))

    end_time = int(dt.strftime("%s"))

    hosts = Host.objects.get_valid_hosts()
    for host in hosts:
        update_host_sla(host, period, start_time, end_time)


def update_host_sla(host, period, start_time, end_time):
    message = 'Updating SLAs for host %s. Period: %s, start_time: %s, end_time: %s'
    logger.debug(message, host, period, start_time, end_time)

    backend = host.get_backend()

    try:
        current_sla = backend.get_sla(host.service_id, start_time, end_time)
        entry, _ = SlaHistory.objects.get_or_create(host=host, period=period)
        entry.value = Decimal(current_sla)
        entry.save()
    except ZabbixBackendError as e:
        logger.warning('Unable to update SLA value for %s. Reason: %s' % (host.service_id, e))

    # update connected events
    try:
        events = backend.get_trigger_events(host.trigger_id, start_time, end_time)
        for event in events:
            event_state = 'U' if int(event['value']) == 0 else 'D'
            entry.events.get_or_create(
                    timestamp=int(event['timestamp']),
                    state=event_state
            )
    except ZabbixBackendError as e:
            logger.warning('Unable to update events for trigger %s. Reason: %s' % (host.trigger_id, e))
