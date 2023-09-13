"""
Django Admin Customisation
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """
    Define the admin page for users
    """
    ordering = ['id']
    list_display = ['email', 'username']
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_superuser',
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login',),
        }
         ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'is_active',
                'is_superuser',)
        }),
    )


admin.site.register(models.User, UserAdmin)
# admin.site.register(models.Receipe)
# admin.site.register(models.Tag)
