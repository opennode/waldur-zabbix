from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

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
    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name='crms', on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')

    @classmethod
    def get_url_name(cls):
        return 'zabbix-hosts'
