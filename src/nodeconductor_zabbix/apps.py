from django.apps import AppConfig

from nodeconductor.structure import SupportedServices


class ZabbixConfig(AppConfig):
    name = 'nodeconductor_zabbix'
    verbose_name = "NodeConductor Zabbix"

    def ready(self):
        ZabbixService = self.get_model('ZabbixService')

        # structure
        from .backend import ZabbixBackend
        SupportedServices.register_backend(ZabbixService, ZabbixBackend)

        # templates
        from nodeconductor.template import TemplateRegistry
        from nodeconductor_zabbix.template import HostProvisionTemplateForm
        TemplateRegistry.register(HostProvisionTemplateForm)
