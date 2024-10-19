from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)
