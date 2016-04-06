from nodeconductor.core.permissions import StaffPermissionLogic
from nodeconductor.structure import perms as structure_perms


PERMISSION_LOGICS = (
    ('nodeconductor_zabbix.ZabbixService', structure_perms.service_permission_logic),
    ('nodeconductor_zabbix.ZabbixServiceProjectLink', structure_perms.service_project_link_permission_logic),
    ('nodeconductor_zabbix.Host', structure_perms.resource_permission_logic),
    ('nodeconductor_zabbix.ITService', structure_perms.resource_permission_logic),
    ('nodeconductor_zabbix.Template', StaffPermissionLogic(any_permission=True)),
    ('nodeconductor_zabbix.Trigger', StaffPermissionLogic(any_permission=True)),
    ('nodeconductor_zabbix.SlaHistory', StaffPermissionLogic(any_permission=True)),
    ('nodeconductor_zabbix.SlaHistoryEvent', StaffPermissionLogic(any_permission=True)),
)
