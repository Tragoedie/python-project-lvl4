from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView
from task_manager.statuses.models import Status
from task_manager.views_for_login import CustomDeleteView, CustomLoginMixin


class StatusesListView(CustomLoginMixin, ListView):
    template_name = 'statuses_list.html'
    model = Status
    context_object_name = 'statuses_list'
    fields = ('name', )


class StatusCreateView(CustomLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'status_create.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created.')
    fields = ('name', )
    denied_without_login_message = _('You are not authorized! Please, log in.')


class StatusUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_update.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully changed.')
    fields = ('name', )


class StatusDeleteView(CustomDeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted.')
    deletion_error_message = _(
        'Can not delete this status - because it is in use.',
    )
