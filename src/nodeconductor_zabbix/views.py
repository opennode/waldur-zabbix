import time

from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from nodeconductor.structure import views as structure_views
from . import models, serializers, filters


class ZabbixServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.ZabbixService.objects.all()
    serializer_class = serializers.ServiceSerializer


class ZabbixServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.ZabbixServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class HostViewSet(structure_views.BaseOnlineResourceViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    filter_backends = (
        filters.HostScopeFilterBackend,
    )

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(resource)

    @detail_route()
    def items_history(self, request, uuid=None):
        host = self.get_object()

        hour = 60 * 60
        now = time.time()
        mapped = {
            'start_timestamp': request.query_params.get('from', int(now - hour)),
            'end_timestamp': request.query_params.get('to', int(now)),
            'segments_count': request.query_params.get('datapoints', 6),
            'item': request.query_params.getlist('item')
        }

        serializer = serializers.StatsSerializer(data={k: v for k, v in mapped.items() if v})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.get_stats(host), status=status.HTTP_200_OK)


class TemplateViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Template.objects.all().select_related('items')
    serializer_class = serializers.TemplateSerializer
    lookup_field = 'uuid'
