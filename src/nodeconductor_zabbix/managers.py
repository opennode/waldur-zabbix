from nodeconductor.core.managers import GenericKeyMixin
from nodeconductor.structure.managers import StructureManager
from nodeconductor.structure.models import Resource


class HostManager(GenericKeyMixin, StructureManager):

    def get_available_models(self):
        """ Return list of models that are acceptable """
        return Resource.get_all_models()
