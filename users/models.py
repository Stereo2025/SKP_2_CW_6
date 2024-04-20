from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    country = models.CharField(max_length=25, verbose_name='Страна', blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', blank=True, null=True)
    verify_code = models.CharField(max_length=20, default='', verbose_name='Код верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.verify_code:
            self.verify_code = ''.join(random.sample('0123456789', 5))
        super().save(*args, **kwargs)

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            (
                'set_is_active',
                'Can deactivate user'
            )
        ]
