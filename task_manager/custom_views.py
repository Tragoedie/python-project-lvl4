from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CustomLoginMixin(LoginRequiredMixin):
    success_url = reverse_lazy('user_login')
    without_login_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.without_login_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class CustomUpdateDeleteMixin(LoginRequiredMixin, AccessMixin):
    success_url = reverse_lazy('users')
    unable_to_change_message = 'You have not permission to change another user.'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != self.request.user.id:
            messages.error(self.request, self.unable_to_change_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
