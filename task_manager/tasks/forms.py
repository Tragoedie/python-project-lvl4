from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta(object):
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'tasks_author',
            'tasks_executor',
            'labels',
        ]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels'),
        }
