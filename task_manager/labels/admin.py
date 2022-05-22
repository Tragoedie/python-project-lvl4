from django.contrib import admin
from task_manager.labels.models import Label


class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_display_links = ('name', )
    search_fields = ('name', )


admin.site.register(Label, LabelAdmin)
