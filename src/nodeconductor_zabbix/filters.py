import django_filters

from nodeconductor.core import filters as core_filters
from nodeconductor.structure import models as structure_models
from nodeconductor.structure.filters import BaseServicePropertyFilter


class HostScopeFilterBackend(core_filters.GenericKeyFilterBackend):

    def get_related_models(self):
        return structure_models.Resource.get_all_models()

    def get_field_name(self):
        return 'scope'


class TriggerFilter(BaseServicePropertyFilter):
    template = core_filters.URLFilter(view_name='zabbix-template-detail', name='template__uuid', distinct=True)
    template_uuid = django_filters.CharFilter(name='template__uuid')


class TemplateFilter(BaseServicePropertyFilter):
    settings = core_filters.URLFilter(view_name='servicesettings-detail', name='settings__uuid', distinct=True)
    settings_uuid = django_filters.CharFilter(name='template__uuid')
