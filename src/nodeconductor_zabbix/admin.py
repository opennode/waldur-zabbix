from django.contrib import admin

from nodeconductor.structure import admin as structure_admin
from .models import ZabbixServiceProjectLink, ZabbixService, Host, SlaHistory, SlaHistoryEvent


class SlaHistoryEventsInline(admin.TabularInline):
    model = SlaHistoryEvent
    fields = ('timestamp', 'state')
    ordering = ('timestamp', )
    extra = 1


class SlaHistoryAdmin(admin.ModelAdmin):
    inlines = (
        SlaHistoryEventsInline,
    )
    list_display = ('itservice', 'period', 'value')
    list_filter = ('itservice', 'period')


admin.site.register(Host, structure_admin.ResourceAdmin)
admin.site.register(ZabbixService, structure_admin.ServiceAdmin)
admin.site.register(ZabbixServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)
admin.site.register(SlaHistory, SlaHistoryAdmin)
