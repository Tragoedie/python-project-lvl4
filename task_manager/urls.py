from django.contrib import admin
from django.urls import include, path
from task_manager import views

urlpatterns = [
    path('', views.main, name='main_page'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('admin/', admin.site.urls),
]
