from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import serializers as rf_serializers

from nodeconductor.core.serializers import HistorySerializer
from nodeconductor.core.utils import datetime_to_timestamp
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
    filter_backends = structure_views.BaseOnlineResourceViewSet.filter_backends + (
        filters.HostScopeFilterBackend,
    )

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(resource)

    @detail_route()
    def items_history(self, request, uuid=None):
        mapped = {
            'start': request.query_params.get('start'),
            'end': request.query_params.get('end'),
            'points_count': request.query_params.get('points_count'),
            'point_list': request.query_params.getlist('point')
        }
        serializer = HistorySerializer(data={k: v for k, v in mapped.items() if v})
        serializer.is_valid(raise_exception=True)

        host = self.get_object()
        invalid_states = (
            models.Host.States.PROVISIONING_SCHEDULED,
            models.Host.States.PROVISIONING,
            models.Host.States.ERRED
        )
        if not host.backend_id or host.state in invalid_states:
            message = 'Unable to get statistics for host in %s state' % host.get_state_display()
            raise rf_serializers.ValidationError(message)

        items = request.query_params.getlist('item')
        items = models.Item.objects.filter(template__hosts=host, name__in=items)

        backend = host.get_backend()
        points = map(datetime_to_timestamp, serializer.get_filter_data())

        stats = []
        for item in items:
            values = backend.get_item_stats(host.backend_id, item, points)
            for point, value in zip(points, values):
                stats.append({
                    'point': point,
                    'item': item.name,
                    'value': value
                })

        return Response(stats, status=status.HTTP_200_OK)


class TemplateViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Template.objects.all().select_related('items')
    serializer_class = serializers.TemplateSerializer
    lookup_field = 'uuid'
