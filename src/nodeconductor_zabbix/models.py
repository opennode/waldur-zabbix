from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from . import managers
from nodeconductor.structure import models as structure_models


class ZabbixService(structure_models.Service):
    projects = models.ManyToManyField(
        structure_models.Project, related_name='zabbix_services', through='ZabbixServiceProjectLink')

    @classmethod
    def get_url_name(cls):
        return 'zabbix'


class ZabbixServiceProjectLink(structure_models.ServiceProjectLink):
    service = models.ForeignKey(ZabbixService)

    class Meta:
        unique_together = ('service', 'project')

    @classmethod
    def get_url_name(cls):
        return 'zabbix-spl'


class Host(structure_models.Resource):
    VISIBLE_NAME_MAX_LENGTH = 64
    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name='crms', on_delete=models.PROTECT)
    visible_name = models.CharField(_('visible name'), max_length=VISIBLE_NAME_MAX_LENGTH)
    interface_parameters = JSONField(blank=True)
    host_group_name = models.CharField(_('host group name'), max_length=64, blank=True)

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')

    objects = managers.HostManager('scope')

    @classmethod
    def get_url_name(cls):
        return 'zabbix-hosts'

    def clean(self):
        # It is impossible to mark service and name unique together at DB level, because host is connected with service
        # through SPL.
        same_service_hosts = Host.objects.filter(service_project_link__service=self.service_project_link.service)
        if same_service_hosts.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(
                'Host with name "%s" already exists at this service. Host name should be unique.' % self.name)
        if same_service_hosts.filter(visible_name=self.visible_name).exclude(pk=self.pk).exists():
            raise ValidationError('Host with visible_name "%s" already exists at this service.'
                                  ' Host name should be unique.' % self.visible_name)

    @classmethod
    def get_visible_name_from_scope(cls, scope):
        """ Generate visible name based on host scope """
        return ('%s-%s' % (scope.uuid.hex, scope.name))[:64]


# Zabbix host name max length - 64
Host._meta.get_field('name').max_length = 64
