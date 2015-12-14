from . import views


def register_in(router):
    router.register(r'zabbix', views.ZabbixServiceViewSet, base_name='zabbix')
    router.register(r'zabbix-hosts', views.HostViewSet, base_name='zabbix-host')
    router.register(r'zabbix-service-project-link', views.ZabbixServiceProjectLinkViewSet, base_name='zabbix-spl')
    router.register(r'zabbix-templates', views.TemplateViewSet, base_name='zabbix-template')
