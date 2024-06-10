from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    

    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)



admin.site.register(User)