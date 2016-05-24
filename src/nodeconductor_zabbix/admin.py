from django.contrib import admin
from django.utils.translation import ungettext

from nodeconductor.core.tasks import send_task
from nodeconductor.structure import admin as structure_admin
from .models import ZabbixServiceProjectLink, ZabbixService, Host, SlaHistory, SlaHistoryEvent, ITService


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
    ordering = ('itservice', 'period')
    list_filter = ('period',)


class HostAdmin(structure_admin.ResourceAdmin):
    actions = ['pull_sla']

    def pull_sla(self, request, queryset):
        send_task('zabbix', 'pull_sla')([host.uuid.hex for host in queryset])

        tasks_scheduled = queryset.count()
        message = ungettext(
            'SLA pulling has been scheduled for one host',
            'SLA pulling has been scheduled for %(tasks_scheduled)d hosts',
            tasks_scheduled
        )
        message = message % {'tasks_scheduled': tasks_scheduled}

        self.message_user(request, message)

    pull_sla.short_description = "Pull SLAs for given Zabbix hosts"


class ITServiceAdmin(structure_admin.ResourceAdmin):
    pass


admin.site.register(Host, HostAdmin)
admin.site.register(ITService, ITServiceAdmin)
admin.site.register(ZabbixService, structure_admin.ServiceAdmin)
admin.site.register(ZabbixServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)
admin.site.register(SlaHistory, SlaHistoryAdmin)
