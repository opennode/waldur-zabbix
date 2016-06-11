from nodeconductor.core.managers import GenericKeyMixin
from nodeconductor.structure.managers import StructureManager
from nodeconductor.structure.models import Resource, ResourceMixin


def filter_active(qs):
    INVALID_STATES = (
        Resource.States.PROVISIONING_SCHEDULED,
        Resource.States.PROVISIONING,
        Resource.States.DELETING,
        Resource.States.ERRED
    )
    return qs.exclude(backend_id='', state__in=INVALID_STATES)


class HostManager(GenericKeyMixin, StructureManager):
    """ Allows to filter and get hosts by generic key """

    def get_available_models(self):
        """ Return list of models that are acceptable """
        return ResourceMixin.get_all_models()
