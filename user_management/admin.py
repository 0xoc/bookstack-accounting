from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'codename']

admin.site.register(UserProfile)
admin.site.register(Permission, PermissionAdmin)