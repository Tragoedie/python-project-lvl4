from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TasksFilter(FilterSet):
    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label'),
    )

    own_tasks = BooleanFilter(
        field_name='tasks_author',
        label=_('Show_own_tasks'),
        method='filter_own_tasks',
        widget=CheckboxInput,
    )

    def filter_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(tasks_author=self.request.user)
        return queryset

    class Meta(object):
        model = Task
        fields = [
            'status',
            'executor',
            'labels',
            'own_tasks',
        ]
