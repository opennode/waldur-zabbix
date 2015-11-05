from rest_framework import serializers

from nodeconductor.structure import serializers as structure_serializers
from nodeconductor.structure import SupportedServices
from . import models


class ServiceSerializer(structure_serializers.BaseServiceSerializer):

    SERVICE_TYPE = SupportedServices.Types.Zabbix
    SERVICE_ACCOUNT_FIELDS = {
        'backend_url': 'Zabbix URL',
        'username': 'Zabbix user username (e.g. Username)',
        'password': 'Zabbix user password (e.g. Password)',
    }
    SERVICE_ACCOUNT_EXTRA_FIELDS = {
        'group_name': 'Zabbix group name for registered hosts. (default: "nodeconductor")',
        'interface_parameters': 'Parameters for hosts interface. (default: {"dns": "", "ip": "0.0.0.0", "main": 1, '
                                '"port": "10050", "type": 1, "useip": 1})',
        'templates_names': 'List of zabbix hosts templates. (default: ["nodeconductor"])',
    }

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.ZabbixService
        view_name = 'zabbix-detail'


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.ZabbixServiceProjectLink
        view_name = 'zabbix-spl-detail'
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'zabbix-detail'},
        }


class HostSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='zabbix-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='zabbix-spl-detail',
        queryset=models.ZabbixServiceProjectLink.objects.all(),
        write_only=True)

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.Host
        view_name = 'zabbix-hosts-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields
