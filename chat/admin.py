from django.contrib import admin

from .models import Room, Message
# Register your models here.

admin.site.register(Message)

@admin.register(Room)
class ProductAdmin(admin.ModelAdmin):
   
    prepopulated_fields = {'slug': ('name',)}