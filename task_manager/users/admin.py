from django.contrib import admin
from task_manager.users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
