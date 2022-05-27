from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.custom_views import CustomLoginMixin
from task_manager.labels.models import Label


class LabelsListView(CustomLoginMixin, ListView):
    template_name = 'labels_list.html'
    model = Label
    context_object_name = 'labels_list'


class LabelCreateView(CustomLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'label_create.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created.')
    fields = ['name']


class LabelUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'label_update.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully changed.')
    fields = ['name']


class LabelDeleteView(CustomLoginMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted.')
    deletion_error_message = _(
        'Can not delete this label - because it is in use.',
    )

    def form_valid(self, form):
        try:
            self.get_object().delete()
        except ProtectedError:
            messages.error(self.request, self.deletion_error_message)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
