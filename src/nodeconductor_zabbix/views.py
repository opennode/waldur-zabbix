from nodeconductor.structure import views as structure_views
from . import models, serializers, filters


class ZabbixServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.ZabbixService.objects.all()
    serializer_class = serializers.ServiceSerializer


class ZabbixServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.ZabbixServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class HostViewSet(structure_views.BaseResourceViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    filter_backends = (
        filters.HostScopeFilterBackend,
    )

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


class TemplateViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Template.objects.all().select_related('items')
    serializer_class = serializers.TemplateSerializer
    lookup_field = 'uuid'
