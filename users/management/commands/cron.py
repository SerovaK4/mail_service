from datetime import datetime

import pytz
import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from client.models import Client
from mail_service.models import Mailing, Log

'''
Реализация отправки рассылок по рассписанию
'''


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status=2)

        tz = pytz.timezone('Europe/Moscow')

        for new_mailing in mailings:
            clients = [client.email for client in Client.objects.filter(user=new_mailing.user)]
            if new_mailing.mailing_time >= datetime.now(tz):
                mail_subject = new_mailing.massage.email_body if new_mailing.massage is not None else 'Рассылка'
                message = new_mailing.massage.email_theme if new_mailing.massage is not None else 'Вам назначена рассылка'
                try:
                    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                    log = Log.objects.create(attempt_date=datetime.now(tz), status='Успешно', server_response='200')
                    log.save()
                except smtplib.SMTPException as err:
                    log = Log.objects.create(attempt_date=datetime.now(tz), status='Ошибка', server_response=err)
                    log.save()
                    # raise err
                new_mailing.status = 3
                new_mailing.save()
