from nodeconductor.core import NodeConductorExtension


class ZabbixExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_zabbix'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
