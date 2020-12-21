from django.contrib import admin

from auth_path.models import Uid


@admin.register(Uid)
class UidAdmin(admin.ModelAdmin):
    list_display = ('uid', 'user')
