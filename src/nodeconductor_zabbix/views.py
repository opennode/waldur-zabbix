from nodeconductor.structure import views as structure_views
from . import models, serializers


class ZabbixServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.ZabbixService.objects.all()
    serializer_class = serializers.ServiceSerializer


class ZabbixServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.ZabbixServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class HostViewSet(structure_views.BaseResourceViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(resource)

    # User can only create and delete Hosts. He cannot stop them.
    @structure_views.safe_operation(valid_state=models.Host.States.ONLINE)
    def destroy(self, request, resource, uuid=None):
        if resource.backend_id:
            backend = resource.get_backend()
            backend.destroy(resource)
        else:
            self.perform_destroy(resource)
