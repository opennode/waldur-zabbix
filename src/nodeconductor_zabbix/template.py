import json

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from rest_framework import serializers

from nodeconductor.core.fields import JsonField
from nodeconductor.template.forms import ServiceTemplateForm, ResourceTemplateForm
from nodeconductor.template.serializers import BaseResourceTemplateSerializer, BaseServiceTemplateSerializer
from . import models


class NestedHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """ Represents object as {'url': <object_url>} """

    def to_internal_value(self, data):
        return super(NestedHyperlinkedRelatedField, self).to_internal_value(data.get('url'))

    def to_representation(self, value):
        return {'url': super(NestedHyperlinkedRelatedField, self).to_representation(value)}


class HostProvisionTemplateForm(ResourceTemplateForm):
    service = forms.ModelChoiceField(
        label='Zabbix service', queryset=models.ZabbixService.objects.all(), required=False)
    name = forms.CharField(label='Name', required=False)
    visible_name = forms.CharField(label='Visible name', required=False)
    host_group_name = forms.CharField(label='Host group name', required=False)
    scope = forms.CharField(label='Host scope', required=False)
    agreed_sla = forms.FloatField(required=False)
    templates = forms.ModelMultipleChoiceField(
        models.Template.objects.all().order_by('name'),
        label='templates',
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Templates', is_stacked=False))

    class Meta(ResourceTemplateForm.Meta):
        fields = ResourceTemplateForm.Meta.fields + ('name', 'visible_name', 'host_group_name')

    class Serializer(BaseResourceTemplateSerializer):
        service = serializers.HyperlinkedRelatedField(
            view_name='zabbix-detail',
            queryset=models.ZabbixService.objects.all(),
            lookup_field='uuid',
            required=False,
        )
        name = serializers.CharField(required=False)
        visible_name = serializers.CharField(required=False)
        host_group_name = serializers.CharField(required=False)
        scope = serializers.CharField(required=False)
        templates = serializers.ListField(
            child=NestedHyperlinkedRelatedField(
                view_name='zabbix-template-detail',
                lookup_field='uuid',
                queryset=models.Template.objects.all()),
            required=False,
        )

    @classmethod
    def get_serializer_class(cls):
        return cls.Serializer

    @classmethod
    def get_model(cls):
        return models.Host


class ITServiceProvisionTemplateForm(ResourceTemplateForm):
    name = forms.CharField(label='Name', required=False)
    service = forms.ModelChoiceField(
        label='Zabbix service', queryset=models.ZabbixService.objects.all(), required=False)
    host = forms.CharField(label='ITService host', required=False)
    algorithm = forms.ChoiceField(choices=[(v, v) for _, v in models.ITService.Algorithm.CHOICES], required=False)
    sort_order = forms.IntegerField(initial=1)
    is_main = forms.BooleanField(initial=True)
    trigger = forms.ModelChoiceField(
        queryset=models.Trigger.objects.all().order_by('template__name', 'name'), required=False)
    agreed_sla = forms.FloatField()

    class Meta(ResourceTemplateForm.Meta):
        fields = ResourceTemplateForm.Meta.fields + ('host',)

    class Serializer(BaseResourceTemplateSerializer):
        service = serializers.HyperlinkedRelatedField(
            view_name='zabbix-detail',
            queryset=models.ZabbixService.objects.all(),
            lookup_field='uuid',
            required=False,
        )
        name = serializers.CharField(required=False)
        sort_order = serializers.IntegerField(initial=1)
        is_main = serializers.BooleanField(initial=True)
        algorithm = serializers.CharField(required=False)
        host = serializers.CharField(required=False)
        trigger = serializers.HyperlinkedRelatedField(
            view_name='zabbix-trigger-detail',
            queryset=models.Trigger.objects.all(),
            lookup_field='uuid',
            required=False,
        )
        agreed_sla = serializers.FloatField(required=False)

    @classmethod
    def get_serializer_class(cls):
        return cls.Serializer

    @classmethod
    def get_model(cls):
        return models.ITService


class ZabbixServiceCreationTemplateForm(ServiceTemplateForm):
    name = forms.CharField()
    backend_url = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()

    host_group_name = forms.CharField(required=False)
    interface_parameters = forms.CharField(required=False, widget=forms.Textarea())
    database_parameters = forms.CharField(required=False, widget=forms.Textarea())

    def _clean_json(self, field_name):
        jdata = self.cleaned_data[field_name]
        if not jdata:
            return jdata
        try:
            json.loads(jdata)
        except:
            raise forms.ValidationError('Invalid data in "%s"' % jdata)
        return jdata

    def clean_interface_parameters(self):
        return self._clean_json('interface_parameters')

    def clean_database_parameters(self):
        return self._clean_json('database_parameters')

    class Serializer(BaseServiceTemplateSerializer):
        name = serializers.CharField()
        backend_url = serializers.CharField()
        username = serializers.CharField()
        password = serializers.CharField()

        host_group_name = serializers.CharField(required=False)
        interface_parameters = JsonField(required=False)
        database_parameters = JsonField(required=False)

        def to_internal_value(self, data):
            internal_values = super(ZabbixServiceCreationTemplateForm.Serializer, self).to_internal_value(data)
            json_fields = 'interface_parameters', 'database_parameters'
            for key, value in internal_values.items():
                if key in json_fields:
                    internal_values[key] = json.dumps(value)
            return internal_values

    @classmethod
    def get_serializer_class(cls):
        return cls.Serializer

    @classmethod
    def get_model(cls):
        return models.ZabbixService

    @classmethod
    def post_create(cls, template, zabbix_service):
        database_parameters = zabbix_service.settings.options.get('database_parameters', {})
        if isinstance(database_parameters, basestring):
            zabbix_service.settings.options['database_parameters'] = json.loads(database_parameters)
            zabbix_service.settings.save()
