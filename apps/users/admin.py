from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _ # this rejister a text for translation
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
   
    list_display = ('username', 'email', 'is_staff', 'is_active','is_verified','last_login')
    list_filter = ('is_staff', 'is_active','is_verified')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Account information'), {'fields': ('first_name', 'last_name', 'email','phone_number')}),
        (_('Accessibility'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser','is_verified',
                'groups', 'user_permissions',
            ),
        }),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('username', 'email',"phone_number")
    ordering = ('username',)
