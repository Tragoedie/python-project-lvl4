from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import CustomUser


class RegisterUpdateForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
