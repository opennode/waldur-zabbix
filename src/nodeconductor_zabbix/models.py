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

    @classmethod
    def get_url_name(cls):
        return 'zabbix-spl'


class Host(structure_models.Resource):
    VISIBLE_NAME_MAX_LENGTH = 64
    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name='hosts', on_delete=models.PROTECT)
    visible_name = models.CharField(_('visible name'), max_length=VISIBLE_NAME_MAX_LENGTH)
    interface_parameters = JSONField(blank=True)
    host_group_name = models.CharField(_('host group name'), max_length=64, blank=True)
    templates = models.ManyToManyField('Template', related_name='hosts')

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')

    objects = managers.HostManager('scope')

    @classmethod
    def get_url_name(cls):
        return 'zabbix-host'

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


class Template(structure_models.ServiceProperty):
    @classmethod
    def get_url_name(cls):
        return 'zabbix-template'


class Trigger(structure_models.ServiceProperty):
    template = models.ForeignKey(Template, related_name='triggers')


# Zabbix trigger name max length - 255
Trigger._meta.get_field('name').max_length = 255


class ITService(structure_models.Resource):
    host = models.ForeignKey(Host)
    trigger = models.ForeignKey(Trigger)
    agreed_sla = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    service_project_link = models.ForeignKey(ZabbixServiceProjectLink, related_name='itservice', on_delete=models.PROTECT)

    @classmethod
    def get_url_name(cls):
        return 'zabbix-itservice'


class Item(models.Model):
    class ValueTypes:
        FLOAT = 0
        CHAR = 1
        LOG = 2
        INTEGER = 3
        TEXT = 4

        CHOICES = (
            (FLOAT, 'Numeric (float)'),
            (CHAR, 'Character'),
            (LOG, 'Log'),
            (INTEGER, 'Numeric (unsigned)'),
            (TEXT, 'Text')
        )

    name = models.CharField(max_length=255)
    template = models.ForeignKey(Template, related_name='items')
    backend_id = models.CharField(max_length=64)
    value_type = models.IntegerField(choices=ValueTypes.CHOICES)
    units = models.CharField(max_length=255)
    history = models.IntegerField()
    delay = models.IntegerField()

    def is_byte(self):
        return self.units == 'B'


class SlaHistory(models.Model):
    host = models.ForeignKey(Host)
    period = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=11, decimal_places=4, null=True, blank=True)

    class Meta:
        verbose_name = 'SLA history'
        verbose_name_plural = 'SLA histories'
        unique_together = ('host', 'period')

    def __str__(self):
        return 'SLA for %s during %s: %s' % (self.scope, self.period, self.value)


class SlaHistoryEvent(models.Model):
    EVENTS = (
        ('U', 'DOWN'),
        ('D', 'UP'),
    )

    history = models.ForeignKey(SlaHistory, related_name='events')
    timestamp = models.IntegerField()
    state = models.CharField(max_length=1, choices=EVENTS)

    def __str__(self):
        return '%s - %s' % (self.timestamp, self.state)
