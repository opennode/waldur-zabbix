import factory

from django.core.urlresolvers import reverse

from nodeconductor.structure.tests import factories as structure_factories

from .. import models


class ZabbixServiceFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = models.ZabbixService

    name = factory.Sequence(lambda n: 'service%s' % n)
    settings = factory.SubFactory(structure_factories.ServiceSettingsFactory)
    customer = factory.SubFactory(structure_factories.CustomerFactory)

    @classmethod
    def get_url(cls, service=None, action=None):
        if service is None:
            service = ZabbixServiceFactory()
        url = 'http://testserver' + reverse('zabbix-detail', kwargs={'uuid': service.uuid})
        return url if action is None else url + action + '/'

    @classmethod
    def get_list_url(cls):
        return 'http://testserver' + reverse('zabbix-list')


class ZabbixServiceProjectLinkFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = models.ZabbixServiceProjectLink

    service = factory.SubFactory(ZabbixServiceFactory)
    project = factory.SubFactory(structure_factories.ProjectFactory)

    @classmethod
    def get_url(cls, spl=None):
        if spl is None:
            spl = ZabbixServiceProjectLinkFactory()
        return 'http://testserver' + reverse('zabbix-spl-detail', kwargs={'pk': spl.pk})
