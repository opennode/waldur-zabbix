from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals

from nodeconductor.structure import SupportedServices, models as structure_models


class ZabbixConfig(AppConfig):
    name = 'nodeconductor_zabbix'
    verbose_name = "NodeConductor Zabbix"
    service_name = 'Zabbix'

    def ready(self):
        # structure
        from .backend import ZabbixBackend
        SupportedServices.register_backend(ZabbixBackend)

        # templates
        from nodeconductor.template import TemplateRegistry
        from nodeconductor_zabbix.template import HostProvisionTemplateForm
        TemplateRegistry.register(HostProvisionTemplateForm)

        from . import handlers
        for index, resource_model in enumerate(structure_models.Resource.get_all_models()):
            signals.post_save.connect(
                handlers.update_hosts_visible_name_on_scope_name_change,
                sender=resource_model,
                dispatch_uid='nodeconductor_zabbix.handlers.update_hosts_visible_name_on_scope_name_change_%s_%s' % (
                              index, resource_model.__name__)
            )

            signals.pre_delete.connect(
                handlers.delete_hosts_on_scope_deletion,
                sender=resource_model,
                dispatch_uid='nodeconductor_zabbix.handlers.delete_hosts_on_scope_deletion_%s_%s' % (
                              index, resource_model.__name__)
            )
