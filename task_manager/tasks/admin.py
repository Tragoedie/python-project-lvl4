from django.contrib import admin
from task_manager.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'status',
        'tasks_author',
        'executor',
        'created',
    )
    list_display_links = ('name', 'tasks_author', 'created')
    search_fields = ('name', 'tasks_author', 'executor')


admin.site.register(Task, TaskAdmin)
