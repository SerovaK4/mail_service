from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    email_theme = models.CharField(max_length=250, verbose_name='Тема письма')
    email_body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.email_theme}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):

    TITLE_CHOICES_PERIODICITY = [
        (1, 'Раз в день'),
        (2, 'Раз в неделю',),
        (3, 'Раз в месяц',),
    ]

    TITLE_CHOICES_STATUS = [
        (1, 'Создана'),
        (2, 'Запущена',),
        (3, 'Завершена',),
    ]

    mailing_time = models.DateTimeField(verbose_name="Время рассылки", default=timezone.now)
    periodicity = models.PositiveSmallIntegerField(verbose_name="Периодичность", choices=TITLE_CHOICES_PERIODICITY, default=1)
    status = models.PositiveSmallIntegerField(verbose_name='Статус рассылки', choices=TITLE_CHOICES_STATUS, default=1)
    massage = models.ForeignKey(Message, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    attempt_date = models.DateTimeField(verbose_name='Дата последней попытки')
    status = models.CharField(max_length=100, verbose_name='Статус попытки')
    server_response = models.TextField(max_length=100, verbose_name="Ответ почтового сервера", **NULLABLE)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'