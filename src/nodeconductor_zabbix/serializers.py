from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from nodeconductor.core.fields import JsonField, MappedChoiceField
from nodeconductor.core.serializers import GenericRelatedField, HyperlinkedRelatedModelSerializer
from nodeconductor.core.utils import datetime_to_timestamp
from nodeconductor.monitoring.utils import get_period
from nodeconductor.structure import serializers as structure_serializers, models as structure_models

from . import models, backend


class ServiceSerializer(structure_serializers.BaseServiceSerializer):

    SERVICE_ACCOUNT_FIELDS = {
        'backend_url': 'Zabbix API URL (e.g. http://example.com/zabbix/api_jsonrpc.php)',
        'username': 'Zabbix user username (e.g. admin)',
        'password': 'Zabbix user password (e.g. zabbix)',
    }
    SERVICE_ACCOUNT_EXTRA_FIELDS = {
        'host_group_name': 'Zabbix host group name for registered hosts. (default: "nodeconductor")',
        'interface_parameters': 'Default parameters for hosts interface (will be used if interface is not specified in '
                                'host). (default: {"dns": "", "ip": "0.0.0.0", "main": 1, "port": "10050", "type": 1, '
                                '"useip": 1})',
        'templates_names': 'List of Zabbix hosts templates. (default: ["NodeConductor"])',
        'database_parameters': 'Zabbix database parameters. (default: {"host": "localhost", "port": "3306", '
                               '"name": "zabbix", "user": "admin", "password": ""})'
    }

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.ZabbixService
        view_name = 'zabbix-detail'

    def get_fields(self):
        fields = super(ServiceSerializer, self).get_fields()
        fields['host_group_name'].default = backend.ZabbixBackend.DEFAULT_HOST_GROUP_NAME
        fields['templates_names'] = JsonField(
            default=backend.ZabbixBackend.DEFAULT_TEMPLATES_NAMES,
            help_text=self.SERVICE_ACCOUNT_EXTRA_FIELDS['templates_names'],
            write_only=True,
        )
        fields['interface_parameters'] = JsonField(
            default=backend.ZabbixBackend.DEFAULT_INTERFACE_PARAMETERS,
            help_text=self.SERVICE_ACCOUNT_EXTRA_FIELDS['interface_parameters'],
            write_only=True,
        )
        fields['database_parameters'] = JsonField(
            default=backend.ZabbixBackend.DEFAULT_DATABASE_PARAMETERS,
            help_text=self.SERVICE_ACCOUNT_EXTRA_FIELDS['database_parameters'],
            write_only=True,
        )
        fields['backend_url'].required = True
        fields['username'].required = True
        fields['password'].required = True
        return fields


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.ZabbixServiceProjectLink
        view_name = 'zabbix-spl-detail'
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'zabbix-detail'},
        }


class TemplateSerializer(structure_serializers.BasePropertySerializer):

    items = serializers.SerializerMethodField()
    triggers = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Template
        view_name = 'zabbix-template-detail'
        fields = ('url', 'uuid', 'name', 'items', 'triggers', 'settings')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'settings': {'lookup_field': 'uuid'},
        }

    def get_items(self, template):
        return template.items.all().values_list('name', flat=True)

    def get_triggers(self, template):
        return template.triggers.all().values_list('name', flat=True)


class NestedTemplateSerializer(TemplateSerializer, HyperlinkedRelatedModelSerializer):

    class Meta(TemplateSerializer.Meta):
        pass


class HostSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='zabbix-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='zabbix-spl-detail',
        queryset=models.ZabbixServiceProjectLink.objects.all())

    # visible name could be populated from scope, so we need to mark it as not required
    visible_name = serializers.CharField(required=False)
    scope = GenericRelatedField(related_models=structure_models.Resource.get_all_models(), required=False)
    templates = NestedTemplateSerializer(
        queryset=models.Template.objects.all().prefetch_related('items'), many=True, required=False)

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.Host
        view_name = 'zabbix-host-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + (
            'visible_name', 'interface_parameters', 'host_group_name', 'scope', 'templates')

    def get_resource_fields(self):
        return super(HostSerializer, self).get_resource_fields() + ['scope']

    def validate(self, attrs):
        # initiate name and visible name from scope if it is defined and check that they are not empty
        if 'scope' in attrs:
            attrs['visible_name'] = models.Host.get_visible_name_from_scope(attrs['scope'])
        if not attrs.get('visible_name') and self.instance is None:
            raise serializers.ValidationError('Visible name or scope should be defined.')
        # model validation
        if self.instance is not None:
            for name, value in attrs.items():
                setattr(self.instance, name, value)
            self.instance.clean()
        else:
            instance = models.Host(**{k: v for k, v in attrs.items() if k != 'templates'})
            instance.clean()
        return attrs

    def create(self, validated_data):
        templates = validated_data.pop('templates', None)
        with transaction.atomic():
            host = super(HostSerializer, self).create(validated_data)
            # get default templates from service settings if they are not defined
            if templates is None:
                templates_names = host.service_project_link.service.settings.options.get(
                    'templates_names', backend.ZabbixBackend.DEFAULT_TEMPLATES_NAMES)
                templates = models.Template.objects.filter(
                    settings=host.service_project_link.service.settings,
                    name__in=templates_names
                )
            for template in templates:
                host.templates.add(template)

        return host

    def update(self, host, validated_data):
        templates = validated_data.pop('templates', None)
        with transaction.atomic():
            host = super(HostSerializer, self).update(host, validated_data)
            if templates is not None:
                host.templates.clear()
                for template in templates:
                    host.templates.add(template)

        return host


class ITServiceSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='zabbix-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='zabbix-spl-detail',
        queryset=models.ZabbixServiceProjectLink.objects.all())

    host = serializers.HyperlinkedRelatedField(
        view_name='zabbix-host-detail',
        queryset=models.Host.objects.all(),
        lookup_field='uuid')

    trigger = serializers.HyperlinkedRelatedField(
        view_name='zabbix-trigger-detail',
        queryset=models.Trigger.objects.order_by('name').select_related('settings'),
        lookup_field='uuid')

    algorithm = MappedChoiceField(
        choices={v: v for _, v in models.ITService.Algorithm.CHOICES},
        choice_mappings={v: k for k, v in models.ITService.Algorithm.CHOICES},
    )
    trigger_name = serializers.ReadOnlyField(source='trigger.name')
    actual_sla = serializers.SerializerMethodField()

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.ITService
        view_name = 'zabbix-itservice-detail'
        fields = structure_serializers.BaseResourceSerializer.Meta.fields + (
            'host', 'algorithm', 'sort_order', 'agreed_sla', 'actual_sla', 'trigger', 'trigger_name', 'is_main')

    # XXX: Should we display sla here?
    def get_actual_sla(self, itservice):
        key = 'itservice_sla_map'
        if key not in self.context:
            qs = models.SlaHistory.objects.filter(period=get_period(self.context['request']))
            if isinstance(self.instance, list):
                qs = qs.filter(itservice__in=self.instance)
            else:
                qs = qs.filter(itservice=self.instance)
            self.context[key] = {q.itservice_id: q.value for q in qs}

        return self.context[key].get(itservice.id)

    def validate(self, attrs):
        host = attrs.get('host')
        if host:
            trigger = attrs['trigger']

            if host and not host.templates.filter(id=trigger.template_id).exists():
                raise serializers.ValidationError("Host templates should contain trigger's template")

            if host.service_project_link != attrs['service_project_link']:
                raise serializers.ValidationError('Host and IT service should belong to the same SPL.')

        return attrs


class TriggerSerializer(structure_serializers.BasePropertySerializer):
    template = serializers.HyperlinkedRelatedField(
        view_name='zabbix-template-detail',
        read_only=True,
        lookup_field='uuid')

    class Meta(structure_serializers.BasePropertySerializer.Meta):
        model = models.Trigger
        fields = ('url', 'uuid', 'name', 'template')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid', 'view_name': 'zabbix-trigger-detail'},
        }


class SlaHistoryEventSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    state = serializers.CharField()


class ItemsAggregatedValuesSerializer(serializers.Serializer):
    """ Validate input parameters for items_aggregated_values action. """
    start = serializers.IntegerField(default=lambda: datetime_to_timestamp(timezone.now() - timedelta(hours=1)))
    end = serializers.IntegerField(default=lambda: datetime_to_timestamp(timezone.now()))
    method = serializers.ChoiceField(default='MAX', choices=('MIN', 'MAX'))

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if 'start' in data and 'end' in data and data['start'] >= data['end']:
            raise serializers.ValidationError("End must occur after start")
        return data
