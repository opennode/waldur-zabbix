import datetime

from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from nodeconductor.core.serializers import HistorySerializer
from nodeconductor.core.utils import datetime_to_timestamp
from nodeconductor.structure import views as structure_views

from . import models, serializers, filters


class ZabbixServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.ZabbixService.objects.all()
    serializer_class = serializers.ServiceSerializer

    @detail_route(methods=['GET', 'DELETE'])
    def stale_services(self, request, uuid):
        service = self.get_object()
        backend = service.get_backend()
        services = backend.get_stale_services()
        if request.method == 'GET':
            return Response(services, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            all_ids = [service['id'] for service in services]
            ids = [id for id in request.query_params.getlist('id') if id in all_ids]
            if not ids:
                raise ValidationError({'detail': 'Valid services not found.'})
            message = 'Services %s are deleted.' % ', '.join(ids)
            backend.delete_services(ids)
            return Response({'detail': message}, status=status.HTTP_204_NO_CONTENT)


class ZabbixServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.ZabbixServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class BaseZabbixResourceViewSet(structure_views.BaseOnlineResourceViewSet):
    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(resource)


class HostViewSet(BaseZabbixResourceViewSet):
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSerializer
    filter_backends = BaseZabbixResourceViewSet.filter_backends + (
        filters.HostScopeFilterBackend,
    )

    @list_route()
    def aggregated_items_history(self, request):
        stats = self._get_stats(request, self._get_hosts())
        return Response(stats, status=status.HTTP_200_OK)

    @detail_route()
    def items_history(self, request, uuid):
        stats = self._get_stats(request, self._get_hosts(uuid))
        return Response(stats, status=status.HTTP_200_OK)

    def _get_hosts(self, uuid=None):
        hosts = self.get_queryset().get_active_hosts()
        if uuid:
            hosts = hosts.filter(uuid=uuid)
        return hosts

    def _get_stats(self, request, hosts):
        """
        If item list contains several elements, result is ordered by item
        (in the same order as it has been provided in request) and then by time.
        """
        items = request.query_params.getlist('item')
        items = models.Item.objects.filter(template__hosts__in=hosts, name__in=items).distinct()

        points = self._get_points(request)

        stats = []
        for item in items:
            values = self._sum_rows([
                host.get_backend().get_item_stats(host.backend_id, item, points)
                for host in hosts
            ])

            for point, value in zip(points, values):
                stats.append({
                    'point': point,
                    'item': item.name,
                    'value': value
                })
        return stats

    def _get_points(self, request):
        mapped = {
            'start': request.query_params.get('start'),
            'end': request.query_params.get('end'),
            'points_count': request.query_params.get('points_count'),
            'point_list': request.query_params.getlist('point')
        }
        serializer = HistorySerializer(data={k: v for k, v in mapped.items() if v})
        serializer.is_valid(raise_exception=True)
        points = map(datetime_to_timestamp, serializer.get_filter_data())
        return points

    def _sum_rows(self, rows):
        """
        Input: [[1, 2], [10, 20], [None, None]]
        Output: [11, 22]
        """
        def sum_without_none(xs):
            return sum(x for x in xs if x)
        return map(sum_without_none, zip(*rows))


class ITServiceViewSet(BaseZabbixResourceViewSet):
    queryset = models.ITService.objects.all()
    serializer_class = serializers.ITServiceSerializer

    def _get_period(self):
        period = self.request.query_params.get('period')
        if period is None:
            today = datetime.date.today()
            period = '%s-%s' % (today.year, today.month)
        return period

    def get_serializer_context(self):
        """
        Add period to context.
        """
        context = super(ITServiceViewSet, self).get_serializer_context()
        context['period'] = self._get_period()
        return context


class TemplateViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Template.objects.all().select_related('items')
    serializer_class = serializers.TemplateSerializer
    lookup_field = 'uuid'


class TriggerViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Trigger.objects.all()
    serializer_class = serializers.TriggerSerializer
    lookup_field = 'uuid'
    filter_class = filters.TriggerFilter
