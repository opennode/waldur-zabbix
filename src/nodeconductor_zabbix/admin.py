from django.contrib import admin

from nodeconductor.structure import admin as structure_admin
from .models import ZabbixServiceProjectLink, ZabbixService, Host


admin.site.register(Host, structure_admin.ResourceAdmin)
admin.site.register(ZabbixService, structure_admin.ServiceAdmin)
admin.site.register(ZabbixServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)
