from django.contrib import admin

from mail_service.models import Mailing, Message, Log


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email_theme', 'email_body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'periodicity', 'status')


@admin.register(Log)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('attempt_date', 'status', 'server_response')
