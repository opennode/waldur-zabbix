import datetime
from decimal import Decimal
import logging

from celery import shared_task

from nodeconductor.core.tasks import save_error_message, transition, retry_if_false
from nodeconductor.monitoring.models import ResourceItem, ResourceSla, ResourceSlaStateTransition
from nodeconductor.monitoring.utils import format_period

from .backend import ZabbixBackendError
from .models import Host, ITService, Item, SlaHistory

logger = logging.getLogger(__name__)


@shared_task(name='nodeconductor.zabbix.provision_host')
def provision_host(host_uuid):
    begin_host_provision.apply_async(
        args=(host_uuid,),
        link=set_host_online.si(host_uuid),
        link_error=set_host_erred.si(host_uuid)
    )


@shared_task(name='nodeconductor.zabbix.destroy_host')
def destroy_host(host_uuid):
    begin_host_destroy.apply_async(
        args=(host_uuid,),
        link=delete_host.si(host_uuid),
        link_error=set_host_erred.si(host_uuid),
    )


@shared_task(name='nodeconductor.zabbix.update_visible_name')
def update_visible_name(host_uuid):
    host = Host.objects.get(uuid=host_uuid)
    backend = host.get_backend()
    backend.update_host_visible_name(host)


@shared_task
@transition(Host, 'begin_provisioning')
@save_error_message
def begin_host_provision(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.provision_host(host)


@shared_task
@transition(Host, 'begin_deleting')
@save_error_message
def begin_host_destroy(host_uuid, transition_entity=None):
    host = transition_entity
    backend = host.get_backend()
    backend.destroy_host(host)


@shared_task
@transition(Host, 'set_online')
def set_host_online(host_uuid, transition_entity=None):
    host = transition_entity
    if host.scope:
        for config in Host.MONITORING_ITEMS_CONFIGS:
            after_creation_monitoring_item_update.delay(host_uuid, config)
            logger.info('After creation monitoring items update process was started for host %s (%s)',
                        host.visible_name, host.uuid.hex)


@shared_task
@transition(Host, 'set_erred')
def set_host_erred(host_uuid, transition_entity=None):
    pass


@shared_task
def delete_host(host_uuid):
    Host.objects.get(uuid=host_uuid).delete()


@shared_task(name='nodeconductor.zabbix.update_sla')
def update_sla(sla_type):
    if sla_type not in ('yearly', 'monthly'):
        logger.error('Requested unknown SLA type: %s' % sla_type)
        return

    dt = datetime.datetime.now()

    if sla_type == 'yearly':
        period = dt.year
        start_time = int(datetime.datetime.strptime('01/01/%s' % dt.year, '%d/%m/%Y').strftime("%s"))
    else:  # it's a monthly SLA update
        period = format_period(dt)
        month_start = datetime.datetime.strptime('01/%s/%s' % (dt.month, dt.year), '%d/%m/%Y')
        start_time = int(month_start.strftime("%s"))

    end_time = int(dt.strftime("%s"))

    for itservice in ITService.objects.all():
        update_itservice_sla.delay(itservice.pk, period, start_time, end_time)


@shared_task
def update_itservice_sla(itservice_pk, period, start_time, end_time):
    logger.debug('Updating SLAs for IT Service with PK %s. Period: %s, start_time: %s, end_time: %s',
                 itservice_pk, period, start_time, end_time)

    try:
        itservice = ITService.objects.get(pk=itservice_pk)
    except ITService.DoesNotExist:
        logger.warning('Unable to update SLA for IT Service with PK %s, because it is gone', itservice_pk)
        return

    backend = itservice.host.get_backend()

    try:
        current_sla = backend.get_sla(itservice.backend_id, start_time, end_time)
        entry, _ = SlaHistory.objects.get_or_create(itservice=itservice, period=period)
        entry.value = Decimal(current_sla)
        entry.save()

        # Save SLA if IT service is marked as main for host
        if itservice.host and itservice.host.scope and itservice.is_main:
            ResourceSla.objects.update_or_create(
                scope=itservice.host.scope,
                period=period,
                defaults={
                    'value': current_sla,
                    'agreed_value': itservice.agreed_sla
                }
            )

        if itservice.backend_trigger_id:
            # update connected events
            events = backend.get_trigger_events(itservice.backend_trigger_id, start_time, end_time)
            for event in events:
                event_state = 'U' if int(event['value']) == 0 else 'D'
                entry.events.get_or_create(
                    timestamp=int(event['timestamp']),
                    state=event_state
                )

                if itservice.host and itservice.host.scope and itservice.is_main:
                    ResourceSlaStateTransition.objects.get_or_create(
                        scope=itservice.host.scope,
                        period=period,
                        timestamp=int(event['timestamp']),
                        state=int(event['value']) == 0
                    )
    except ZabbixBackendError as e:
        logger.warning(
            'Unable to update SLA for IT Service %s (ID: %s). Reason: %s', itservice.name, itservice.backend_id, e)
    logger.info('Successfully updated SLA for IT Service %s (ID: %s)', itservice.name, itservice.backend_id)


@shared_task(name='nodeconductor.zabbix.provision_itservice')
def provision_itservice(itservice_uuid):
    begin_itservice_provision.apply_async(
        args=(itservice_uuid,),
        link=set_itservice_online.si(itservice_uuid),
        link_error=set_itservice_erred.si(itservice_uuid)
    )


@shared_task
@transition(ITService, 'begin_provisioning')
@save_error_message
def begin_itservice_provision(itservice_uuid, transition_entity=None):
    itservice = transition_entity
    backend = itservice.get_backend()
    backend.provision_itservice(itservice)


@shared_task(name='nodeconductor.zabbix.destroy_itservice')
def destroy_itservice(itservice_uuid):
    begin_itservice_destroy.apply_async(
        args=(itservice_uuid,),
        link=delete_itservice.si(itservice_uuid),
        link_error=set_itservice_erred.si(itservice_uuid),
    )


@shared_task
@transition(ITService, 'begin_deleting')
@save_error_message
def begin_itservice_destroy(itservice_uuid, transition_entity=None):
    itservice = transition_entity
    backend = itservice.get_backend()
    backend.delete_service(itservice.backend_id)


@shared_task
def delete_itservice(itservice_uuid):
    ITService.objects.get(uuid=itservice_uuid).delete()


@shared_task
@transition(ITService, 'set_online')
def set_itservice_online(host_uuid, transition_entity=None):
    pass


@shared_task
@transition(ITService, 'set_erred')
def set_itservice_erred(host_uuid, transition_entity=None):
    pass


@shared_task(name='nodeconductor.zabbix.update_monitoring_items')
def update_monitoring_items():
    """
    Regularly update value of monitored resources
    """
    hosts = Host.objects.filter(object_id__isnull=False, state=Host.States.ONLINE)
    for host in hosts:
        for config in host.MONITORING_ITEMS_CONFIGS:
            update_host_scope_monitoring_items.delay(host.uuid.hex,
                                                     zabbix_item_name=config['zabbix_item_name'],
                                                     monitoring_item_name=config['monitoring_item_name'])
    logger.info('Successfully scheduled monitoring data update for zabbix hosts.')


@shared_task
def update_host_scope_monitoring_items(host_uuid, zabbix_item_name, monitoring_item_name):
    host = Host.objects.get(uuid=host_uuid)
    value = None
    if Item.objects.filter(template__hosts=host, name=zabbix_item_name).exists():
        value = host.get_backend().get_item_last_value(host.backend_id, key=zabbix_item_name)
        ResourceItem.objects.update_or_create(
            scope=host.scope,
            name=monitoring_item_name,
            defaults={'value': value}
        )
    logger.info('Successfully updated monitoring item %s for host %s (%s). Current value: %s.',
                monitoring_item_name, host.visible_name, host.uuid.hex, value)
    return value


@shared_task(max_retries=60, default_retry_delay=60)
@retry_if_false
def after_creation_monitoring_item_update(host_uuid, config):
    item_value = update_host_scope_monitoring_items(
        host_uuid, config['zabbix_item_name'], config['monitoring_item_name'])
    return item_value in config.get('after_creation_update_terminate_values', []) or item_value is None
