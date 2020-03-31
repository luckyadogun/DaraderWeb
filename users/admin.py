from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active',) 
    list_filter = ('date_joined',)
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
