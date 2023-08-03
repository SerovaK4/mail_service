from django.db import models

from users.models import User

from mail_service.models import NULLABLE


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    second_name = models.CharField(max_length=100, verbose_name='отчество')
    email = models.EmailField()
    comment = models.TextField(**NULLABLE)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE, **NULLABLE)

    is_active = models.BooleanField(default=True, **NULLABLE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.second_name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'