from nodeconductor.core.managers import GenericKeyMixin
from nodeconductor.structure.managers import StructureManager
from nodeconductor.structure.models import Resource


class HostManager(GenericKeyMixin, StructureManager):
    """ Allows to filter and get hosts by generic key """

    def get_available_models(self):
        """ Return list of models that are acceptable """
        return Resource.get_all_models()
