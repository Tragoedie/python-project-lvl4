from django.urls import path
from task_manager.users.views import (
    UserDeleteView,
    UserRegisterView,
    UsersListView,
    UserUpdateView,
)

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('create/', UserRegisterView.as_view(), name='user_register'),
    path(
        '<int:pk>/update/',
        UserUpdateView.as_view(),
        name='user_update',
    ),
    path(
        '<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete',
    ),
]
