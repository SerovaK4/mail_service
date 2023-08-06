from django.contrib import admin

from mail_service.models import Mailing
from users.models import User


# Register your models here.


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'avatar')


class ABCAdmin(admin.ModelAdmin):
    fields = ['status', 'user', ]

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name="Мененджер"):
            return ['status', 'user', ]
        elif request.user.is_superuser:
            return [i.name for i in Mailing._meta.fields if i.name != "id"]
        else:
            return []


admin.site.unregister(Mailing)
admin.site.register(Mailing, ABCAdmin)
