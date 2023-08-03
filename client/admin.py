from django.contrib import admin

from client.models import Client


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'second_name', 'email', 'comment', 'user')
