"""
Recursos do site Admin. 
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Movies


class CustomUserAdmin(UserAdmin):
    """Define a pagina de admin."""
    model = User
    ordering = ['id']
    list_display = ['email', 'is_staff', 'is_active']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Movies)