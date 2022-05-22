from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView
from task_manager.labels.models import Label
from task_manager.views_for_login import CustomDeleteView, CustomLoginMixin


class LabelsListView(CustomLoginMixin, ListView):
    template_name = 'labels_list.html'
    model = Label
    context_object_name = 'labels_list'


class LabelCreateView(CustomLoginMixin, SuccessMessageMixin, CreateView):
    template_name = 'label_create.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully created')
    fields = ['name']


class LabelUpdateView(CustomLoginMixin, SuccessMessageMixin, UpdateView):
    template_name = 'label_update.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully changed')
    fields = ['name']


class LabelDeleteView(CustomDeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')
    deletion_error_message = _(
        'Can not delete label because it is in use',
    )
