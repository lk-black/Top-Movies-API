"""
Recursos do site Admin. 
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """Define the admin pages for users."""
    model = User
    ordering = ['id']
    list_display = ['email', 'is_staff', 'is_active']


admin.site.register(User, CustomUserAdmin)