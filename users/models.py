from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(verbose_name='контактный email (логин)', unique=True)
    phone = models.PositiveBigIntegerField(verbose_name='телефон', unique=True)
    birth_date = models.DateField(verbose_name='дата рождения')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    change_date = models.DateTimeField(auto_now=True, verbose_name='дата редактирования', **NULLABLE)
    password = models.CharField(max_length=1000, verbose_name='пароль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'
