from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.custom_views import CustomLoginMixin, CustomUpdateDeleteMixin
from task_manager.users.forms import RegisterUpdateForm
from task_manager.users.models import CustomUser


class UsersListView(ListView):
    template_name = 'users_list.html'
    model = CustomUser
    context_object_name = 'users_list'


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'user_register.html'
    model = CustomUser
    success_url = reverse_lazy('user_login')
    form_class = RegisterUpdateForm
    success_message = _('User successfully registered.')


class UserUpdateView(
    CustomLoginMixin,
    SuccessMessageMixin,
    CustomUpdateDeleteMixin,
    UpdateView,
):
    template_name = 'user_update.html'
    model = CustomUser
    success_url = reverse_lazy('users')
    form_class = RegisterUpdateForm
    success_message = _('User successfully changed')


class UserDeleteView(
    CustomLoginMixin,
    SuccessMessageMixin,
    CustomUpdateDeleteMixin,
    DeleteView,
):
    template_name = 'user_delete.html'
    model = CustomUser
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted.')
    deletion_error_message = _(
        'You can not delete this user - because it is in use.',
    )

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, self.deletion_error_message)
        else:
            messages.success(self.request, self.success_message)
        return redirect(self.success_url)
