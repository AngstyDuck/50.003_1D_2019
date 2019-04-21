from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from createuser.models import Extended_User


admin.site.register(Extended_User, UserAdmin)
