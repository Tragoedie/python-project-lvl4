from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from task_manager.custom_views import CustomLoginMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task
from task_manager.tasks.tasks_filter import TasksFilter


class TasksListView(CustomLoginMixin, FilterView):
    template_name = 'tasks_list.html'
    model = Task
    context_object_name = 'tasks_list'
    filterset_class = TasksFilter


class TaskCreateView(CustomLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created.')

    def form_valid(self, form):
        form.instance.tasks_author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'task_update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully changed.')


class TaskDeleteView(CustomLoginMixin, SuccessMessageMixin, DeleteView):
    template_name = 'task_delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted.')
    unable_to_delete_tasks = _(
        'The task can only be deleted by its author.',
    )

    def form_valid(self, form):
        if self.request.user == self.get_object().tasks_author:
            super().form_valid(form)
        else:
            messages.error(self.request, self.unable_to_delete_tasks)
        return redirect(self.success_url)


class TaskDetailsView(CustomLoginMixin, DetailView):
    model = Task
    template_name = 'task_details.html'
