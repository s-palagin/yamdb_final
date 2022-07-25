from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class YamdbUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'confirmation_code',
        'role',
        'is_staff'
    )


admin.site.register(User, YamdbUserAdmin)
