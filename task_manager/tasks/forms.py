from django import forms
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta(object):
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'tasks_executor',
            'labels',
        ]
