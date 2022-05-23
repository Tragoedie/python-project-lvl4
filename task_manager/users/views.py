from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView
from task_manager.custom_views import CustomDeleteView
from task_manager.users.forms import RegisterUpdateForm
from task_manager.users.models import CustomUser


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'user_login.html'
    success_message = _('You are logged in.')
    next_page = reverse_lazy('main_page')


class UserLogoutView(LogoutView):
    template_name = 'user_logout.html'
    next_page = reverse_lazy('main_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, _('You are logged out.'))
        return super().dispatch(request, *args, **kwargs)


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


class UserUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'user_update.html'
    model = CustomUser
    success_url = reverse_lazy('users')
    form_class = RegisterUpdateForm
    success_message = _('User successfully changed')
    unable_to_change_message = _(
        'You have not permission to change another user.',
    )

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(
                self.request, self.unable_to_change_message,
            )
            return redirect('users')
        return super().get(request, *args, **kwargs)


class UserDeleteView(CustomDeleteView):
    template_name = 'user_delete.html'
    model = CustomUser
    success_url = reverse_lazy('users')
    success_message = _('User successfully deleted.')
    unable_to_change_message = _(
        'You have not permission to deleted another user.',
    )
    deletion_error_message = _(
        'You can not delete this user - because it is in use.',
    )

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object():
            messages.error(
                self.request, self.unable_to_change_message,
            )
            return redirect('users')
        return super().get(request, *args, **kwargs)
