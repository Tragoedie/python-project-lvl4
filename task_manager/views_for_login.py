from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView


class CustomLoginMixin(LoginRequiredMixin):
    without_login_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.without_login_message)
            return redirect('user_login')
        return super().dispatch(request, *args, **kwargs)


class CustomDeleteView(SuccessMessageMixin, CustomLoginMixin, DeleteView):
    deletion_error_message = None
    success_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, self.deletion_error_message,
            )
            return redirect(self.success_url)
