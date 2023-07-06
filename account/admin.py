
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User 


class UserAgentAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )

    list_filter = (
        'first_name',
        'last_name',
    )

admin.site.register(User, UserAgentAdmin)