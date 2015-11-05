import logging
import warnings

import pyzabbix
import requests
from requests.exceptions import RequestException
from requests.packages.urllib3 import exceptions

from nodeconductor.core.tasks import send_task
from nodeconductor.structure import ServiceBackend, ServiceBackendError, models as structure_models


logger = logging.getLogger(__name__)


class ZabbixBackendError(ServiceBackendError):
    pass


class ZabbixBackend(object):

    def __init__(self, settings, *args, **kwargs):
        backend_class = ZabbixDummyBackend if settings.dummy else ZabbixRealBackend
        self.backend = backend_class(settings, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.backend, name)


class ZabbixBaseBackend(ServiceBackend):

    def provision(self, host):
        send_task('zabbix', 'provision')(
            host.uuid.hex,
        )

    def destroy(self, host):
        # Skip stopping, because host can be deleted directly from state ONLINE
        host.state = structure_models.Resource.States.DELETION_SCHEDULED
        host.save()
        send_task('zabbix', 'destroy')(
            host.uuid.hex,
        )


class QuietSession(requests.Session):
    """Session class that suppresses warning about unsafe TLS sessions and clogging the logs.
    Inspired by: https://github.com/kennethreitz/requests/issues/2214#issuecomment-110366218
    """
    def request(self, *args, **kwargs):
        if not kwargs.get('verify', self.verify):
            with warnings.catch_warnings():
                if hasattr(exceptions, 'InsecurePlatformWarning'):  # urllib3 1.10 and lower does not have this warning
                    warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
                warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
                return super(QuietSession, self).request(*args, **kwargs)
        else:
            return super(QuietSession, self).request(*args, **kwargs)


class ZabbixRealBackend(ZabbixBaseBackend):
    """ Zabbix backend methods """

    DEFAULT_GROUP_NAME = 'nodeconductor'
    DEFAULT_TEMPLATES_NAMES = ('nodeconductor',)
    DEFAULT_INTERFACE_PARAMTERS = {
        'dns': '',
        'ip': '0.0.0.0',
        'main': 1,
        'port': '10050',
        'type': 1,
        'useip': 1
    }

    def __init__(self, settings):
        self.api = self._get_api(settings.backend_url, settings.username, settings.password)
        self.options = settings.options or {}
        self.group_name = self.options.get('group_name', self.DEFAULT_GROUP_NAME)
        self.templates_names = self.options.get('templates_names', self.DEFAULT_TEMPLATES_NAMES)
        self.interface_parameters = self.options.get('interface_parameters', self.DEFAULT_INTERFACE_PARAMTERS)

    def sync(self):
        self._get_or_create_group_id(self.group_name)
        for name in self.templates_names:
            self._get_template_id(name)

    def provision_host(self, host):
        templates_ids = [self._get_template_id(name) for name in self.templates_names]
        group_id, _ = self._get_or_create_group_id(self.group_name)
        name = self._get_host_unique_name(host)

        zabbix_host_id, created = self._get_or_create_host_id(
            host_name=name,
            visible_name=host.name,
            group_id=group_id,
            templates_ids=templates_ids,
            interface_parameters=self.interface_parameters
        )

        if not created:
            logger.warning('Host with name "%s" already exists', name)

        host.backend_id = zabbix_host_id
        host.save()

    def destroy_host(self, host):
        host_name = self._get_host_unique_name(host)
        host_exists_before_deletion = self._delete_host_if_exists(host_name)
        if not host_exists_before_deletion:
            logger.warning('Host "%s" (zabbix host name: "%s") cannot be deleted - it does not exist in Zabbix',
                           host.name, host_name)

    def _get_or_create_group_id(self, group_name):
        try:
            exists = self.api.hostgroup.exists(name=group_name)
            if not exists:
                # XXX: group creation code is not tested
                group_id = self.api.hostgroup.create({'name': group_name})['groupids'][0]
                return group_id, True
            else:
                return self.api.hostgroup.get(filter={'name': group_name})[0]['groupid'], False
        except (pyzabbix.ZabbixAPIException, IndexError, KeyError) as e:
            raise ZabbixBackendError('Cannot get or create group with name "%s". Exception: %s' % (group_name, e))

    def _get_template_id(self, template_name):
        try:
            return self.api.template.get(filter={'name': 'Template NodeConductor Instance'})[0]['templateid']
        except (IndexError, KeyError, pyzabbix.ZabbixAPIException) as e:
            raise ZabbixBackendError('Cannot get template with name "%s". Exception: %s' % (template_name, e))

    def _get_host_unique_name(self, host):
        return host.uuid.hex

    def _get_or_create_host_id(self, host_name, visible_name, group_id, templates_ids, interface_parameters):
        """ Create zabbix host with given parameters.

        Return (<host>, <is_created>) tuple as result.
        """
        try:
            if not self.api.host.exists(host=host_name):
                templates = [{'templateid': template_id} for template_id in templates_ids]
                host_parameters = {
                    "host": host_name,
                    "name": visible_name,
                    "interfaces": [interface_parameters],
                    "groups": [{"groupid": group_id}],
                    "templates": templates,
                }
                host = self.api.host.create(host_parameters)['hostids'][0]
                return host, True
            else:
                host = self.api.host.get(filter={'host': host_name})[0]['hostid']
                return host, False
        except (pyzabbix.ZabbixAPIException, RequestException, IndexError, KeyError) as e:
            raise ZabbixBackendError(
                'Cannot get or create host with parameters: %s. Exception: %s' % (host_parameters, str(e)))

    def _delete_host_if_exists(self, host_name):
        """ Delete zabbix host by name.

        Return True if host was deleted successfully, False if host with such name does not exist.
        """
        try:
            hostid = self.api.host.get(filter={'host': host_name})[0]['hostid']
            self.api.host.delete(hostid)
        except (pyzabbix.ZabbixAPIException, RequestException) as e:
            raise ZabbixBackendError('Cannot create delete host with name "%s". Exception: %s' % (host_name, e))
        except IndexError:
            return False
        return True

    def _get_api(self, backend_url, username, password):
        unsafe_session = QuietSession()
        unsafe_session.verify = False

        api = pyzabbix.ZabbixAPI(server=backend_url, session=unsafe_session)
        api.login(username, password)
        return api


class ZabbixDummyBackend(ZabbixBaseBackend):
    pass
