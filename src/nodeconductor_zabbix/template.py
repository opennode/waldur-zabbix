from django import forms
from rest_framework import serializers

from nodeconductor.template.forms import TemplateForm
from nodeconductor.template.serializers import BaseTemplateSerializer
from nodeconductor_zabbix import models


class HostProvisionTemplateForm(TemplateForm):
    service = forms.ModelChoiceField(
        label='Zabbix service', queryset=models.ZabbixService.objects.all(), required=False)
    name = forms.CharField(label='Name', required=False)
    visible_name = forms.CharField(label='Visible name', required=False)
    host_group_name = forms.CharField(label='Host group name', required=False)

    class Meta(TemplateForm.Meta):
        fields = TemplateForm.Meta.fields + ('name', 'visible_name', 'host_group_name')

    class Serializer(BaseTemplateSerializer):
        service = serializers.HyperlinkedRelatedField(
            view_name='zabbix-detail',
            queryset=models.ZabbixService.objects.all(),
            lookup_field='uuid',
            required=False,
        )
        name = serializers.CharField(required=False)
        visible_name = serializers.CharField(required=False)
        host_group_name = serializers.CharField(required=False)

    @classmethod
    def get_serializer_class(cls):
        return cls.Serializer

    @classmethod
    def get_resource_model(cls):
        return models.Host
