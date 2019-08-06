from django.contrib import admin
from .models import *


# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'get_code']


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)
admin.site.register(AccountingDocument)