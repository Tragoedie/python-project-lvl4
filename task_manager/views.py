from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def main(request):
    return render(request, 'main_page.html')


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
