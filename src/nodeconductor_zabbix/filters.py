import django_filters
from django.contrib.contenttypes.models import ContentType

from nodeconductor.core import filters as core_filters
from nodeconductor.monitoring.models import ResourceSla, ResourceItem, ResourceState
from nodeconductor.structure import models as structure_models
from nodeconductor.structure.filters import BaseServicePropertyFilter, ExternalResourceFilterBackend
from nodeconductor_zabbix.utils import get_period


class HostScopeFilterBackend(core_filters.GenericKeyFilterBackend):

    def get_related_models(self):
        return structure_models.Resource.get_all_models()

    def get_field_name(self):
        return 'scope'


class TriggerFilter(BaseServicePropertyFilter):
    template = django_filters.CharFilter(name='template__uuid')


class ResourceStateFilter(django_filters.FilterSet):
    class Meta:
        model = ResourceState
    period = django_filters.CharFilter(name='period')


class SlaFilter(core_filters.BaseExternalFilter):
    """
    Allows to filter or sort resources by actual_sla
    Default period is current year and month.

    Example query parameters for filtering list of OpenStack instances:
    /api/openstack-instances/?actual_sla=90&period=2016-02

    Example query parameters for sorting list of OpenStack instances:
    /api/openstack-instances/?o=actual_sla&period=2016-02
    """
    def filter(self, request, queryset, view):
        period = get_period(request)

        if 'actual_sla' in request.query_params:
            value = request.query_params.get('actual_sla')
            return queryset.filter(sla_items__value=value, sla_items__period=period)

        elif request.query_params.get('o') == 'actual_sla':
            extra = self._get_extra(queryset.model, period)
            return queryset.extra(**extra).order_by('actual_sla')

        else:
            return queryset

    def _get_extra(self, model, period):
        """
        actual_sla column is subquery from SLA table
        """
        template = 'SELECT "value" FROM "{sla_table}" ' \
                   'WHERE "{sla_table}"."object_id" = "{resource_table}"."id" ' \
                   'AND "{sla_table}"."content_type_id" = "{content_type}" ' \
                   'AND "{sla_table}"."period" = %s'

        params = dict(
            sla_table=ResourceSla._meta.db_table,
            resource_table=model._meta.db_table,
            content_type=ContentType.objects.get_for_model(model).id,
        )
        query = template.format(**params)
        extra = dict(
            select={'actual_sla': query},
            select_params=[period]
        )
        return extra


class MonitoringItemFilter(core_filters.BaseExternalFilter):
    """
    Filter and order resources by monitoring item.
    For example, given query dictionary
    {
        'monitoring__installation_state': True
    }
    it produces following query
    {
        'monitoring_item__name': 'installation_state',
        'monitoring_item__value': True
    }

    Example query parameters for sorting list of OpenStack instances:
    /api/openstack-instances/?o=monitoring__installation_state
    """
    def filter(self, request, queryset, view):
        for key in request.query_params.keys():
            item_name = self._get_item_name(key)
            if item_name:
                value = request.query_params.get(key)
                queryset = queryset.filter(monitoring_items__name=item_name,
                                           monitoring_items__value=value)

        order_by = request.query_params.get('o')
        item_name = self._get_item_name(order_by)
        if item_name:
            extra = self._get_extra(queryset.model, item_name)
            return queryset.extra(**extra).order_by('monitoring_item')

        return queryset

    def _get_item_name(self, key):
        if key and key.startswith('monitoring__'):
            _, item_name = key.split('__', 1)
            return item_name

    def _get_extra(self, model, item_name):
        """
        monitoring_item column is subquery from item table
        """
        template = 'SELECT "value" FROM "{item_table}" ' \
                   'WHERE "{item_table}"."object_id" = "{resource_table}"."id" ' \
                   'AND "{item_table}"."content_type_id" = "{content_type}" ' \
                   'AND "{item_table}"."name" = %s'

        params = dict(
            item_table=ResourceItem._meta.db_table,
            resource_table=model._meta.db_table,
            content_type=ContentType.objects.get_for_model(model).id,
        )
        query = template.format(**params)
        extra = dict(
            select={'monitoring_item': query},
            select_params=[item_name]
        )
        return extra


ExternalResourceFilterBackend.register(SlaFilter())
ExternalResourceFilterBackend.register(MonitoringItemFilter())
