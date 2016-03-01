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
    template = django_filters.CharFilter(name='template__uuid')
