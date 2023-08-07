from django.core.management import BaseCommand
from django.utils import timezone

from client.models import Client
from mail_service.models import Mailing, Message
from users.models import User

"""Наполнение базы Рассылки, Клиенты, Сообщения"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        message_list = [
            {'id': 3, 'email_theme': 'Освежите свой образ - скидка 30% на коллекцию новейших парфюмов!',
             'email_body': 'Любите быть в центре внимания? Тогда у вас есть прекрасный шанс обновить свой аромат с нашей коллекцией новейших парфюмов. У нас имеются уникальные композиции для каждого вкуса, и теперь вы можете приобрести любой из них с скидкой 30%! Насладитесь своим путешествием в мир ароматов, не переплачивая!'},
            {'id': 2, 'email_theme': 'Заряд энергии в каждой чашке! Кофе с максимальной скидкой!', 'email_body': 'Вы любите настоящий аромат кофе и ощущение бодрости каждое утро? Мы предлагаем вам уникальную коллекцию кофейных смесей с максимальной выгодой. Сейчас у вас есть шанс приобрести любимый кофе с максимальной скидкой! Зарядите себя энергией каждый день, наслаждаясь богатым вкусом и ароматом!'}
        ]
        message_for_create = []

        for message in message_list:
            message_for_create.append(
                Message(**message)
            )

        Message.objects.bulk_create(message_for_create)

        mailing_list = [
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 1, 'massage': Message.objects.get(pk=1)},
            {'mailing_time': timezone.now(), 'periodicity': 2, 'status': 2, 'massage': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 3, 'status': 3, 'massage': Message.objects.get(pk=1)},
            {'mailing_time': timezone.now(), 'periodicity': 3, 'status': 2, 'massage': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 1, 'massage': Message.objects.get(pk=1)},
            {'mailing_time': timezone.now(), 'periodicity': 2, 'status': 3, 'massage': Message.objects.get(pk=2)},
            {'mailing_time': timezone.now(), 'periodicity': 2, 'status': 3, 'massage': Message.objects.get(pk=1)},
            {'mailing_time': timezone.now(), 'periodicity': 1, 'status': 2},
        ]
        mailing_for_create = []

        for mailing in mailing_list:
            mailing_for_create.append(
                Mailing(**mailing)
            )

        Mailing.objects.bulk_create(mailing_for_create)

        client_list = [
            {'first_name': 'Sergey', 'last_name': 'Sergeev', 'second_name': 'Sergeevich', 'email': 'SergeySergeev@sky.pro'},
            {'first_name': 'Matvey', 'last_name': 'Matveev', 'second_name': 'Matveevich', 'email': 'Matveev12@sky.pro'},
            {'first_name': 'Ivan', 'last_name': 'Ivanov', 'second_name': 'Ivanovich', 'email': 'IvanIvanov@sky.pro'},
            {'first_name': 'Petr', 'last_name': 'Petrov', 'second_name': 'Petrovich', 'email': 'PetrPetrov@sky.pro'},
            {'first_name': 'Igor', 'last_name': 'Igrov', 'second_name': 'Igorevich', 'email': 'tIgorIgorev@sky.pro'},
            ]
        client_for_create = []

        for client in client_list:
            client_for_create.append(
                Client(**client)
            )

        Client.objects.bulk_create(client_for_create)
