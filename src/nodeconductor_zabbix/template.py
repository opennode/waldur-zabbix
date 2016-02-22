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
    scope = forms.CharField(label='Host scope', required=False)
    agreed_sla = forms.FloatField(required=False)

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
        scope = serializers.CharField(required=False)

    @classmethod
    def get_serializer_class(cls):
        return cls.Serializer

    @classmethod
    def get_resource_model(cls):
        return models.Host


class ITServiceProvisionTemplateForm(TemplateForm):
    name = forms.CharField(label='Name', required=False)
    service = forms.ModelChoiceField(
        label='Zabbix service', queryset=models.ZabbixService.objects.all(), required=False)
    host = forms.CharField(label='ITService host', required=False)
    algorithm = forms.ChoiceField(choices=[(v, v) for _, v in models.ITService.Algorithm.CHOICES], required=False)
    sort_order = forms.IntegerField(initial=1)
    is_main = forms.BooleanField(initial=True)
    trigger = forms.ModelChoiceField(queryset=models.Trigger.objects.all().order_by('name'), required=False)
    agreed_sla = forms.FloatField()

    class Meta(TemplateForm.Meta):
        fields = TemplateForm.Meta.fields + ('host',)

    class Serializer(BaseTemplateSerializer):
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
    def get_resource_model(cls):
        return models.ITService
