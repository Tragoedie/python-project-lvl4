from django.urls import path
from task_manager.users.views import (
    UserDeleteView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UsersListView,
    UserUpdateView,
)

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
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
