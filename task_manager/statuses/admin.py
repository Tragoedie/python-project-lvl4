from django.contrib import admin
from task_manager.statuses.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_display_links = ('name', 'created')
    search_fields = ('name', )


admin.site.register(Status, StatusAdmin)
