from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.custom_views import CustomLoginMixin
from task_manager.statuses.models import Status


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


class StatusUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_update.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully changed.')
    fields = ('name', )


class StatusDeleteView(DeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted.')
    deletion_error_message = _(
        'Can not delete this status - because it is in use.',
    )

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.deletion_error_message)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
