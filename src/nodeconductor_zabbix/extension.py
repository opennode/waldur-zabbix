from nodeconductor.core import NodeConductorExtension


class ZabbixExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_zabbix'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {
            'update-monthly-slas': {
                'task': 'nodeconductor_zabbix.tasks.update_sla',
                'schedule': timedelta(minutes=5),
                'args': ('monthly',),
            },
            'update-yearly-slas': {
                'task': 'nodeconductor_zabbix.tasks.update_sla',
                'schedule': timedelta(minutes=10),
                'args': ('yearly',),
            }
        }
