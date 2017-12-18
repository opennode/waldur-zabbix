from waldur_core.core import WaldurExtension


class ZabbixExtension(WaldurExtension):

    class Settings:
        WALDUR_ZABBIX = {
            'SMS_SETTINGS': {
                # configurations for default SMS notifications.
                'SMS_EMAIL_FROM': None,
                'SMS_EMAIL_RCPT': None,
            },
        }

    @staticmethod
    def django_app():
        return 'waldur_zabbix'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {
            'update-monthly-slas': {
                'task': 'waldur_core.zabbix.update_sla',
                'schedule': timedelta(minutes=5),
                'args': ('monthly',),
            },
            'update-yearly-slas': {
                'task': 'waldur_core.zabbix.update_sla',
                'schedule': timedelta(minutes=10),
                'args': ('yearly',),
            },
            'update-monitoring-items': {
                'task': 'waldur_core.zabbix.update_monitoring_items',
                'schedule': timedelta(minutes=10),
            },
            'pull-zabbix-hosts': {
                'task': 'waldur_core.zabbix.pull_hosts',
                'schedule': timedelta(minutes=30),
            },
        }
