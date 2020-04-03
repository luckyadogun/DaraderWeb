from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import (
    UserCreationForm,
    UserChangeForm)


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'date_joined', 'is_active') 
    list_filter = ('date_joined',)
    readonly_fields = ('password',)
    fieldsets = (
        (None, {
            'fields': (
                'email', 'username', 
                'password', 'is_staff', 
                'is_active', 'is_account_manager'
            )}
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 
                'password1', 'password2',
                'is_staff', 'is_account_manager')
        }),
    )

    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
