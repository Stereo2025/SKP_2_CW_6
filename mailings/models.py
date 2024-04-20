from django.conf import settings
from django.db import models


PERIODISITY_CHOISES = (
    ('day', 'Раз в день'),
    ('week', 'Раз в неделю'),
    ('month', 'Раз в месяц'),
)

STATUS_CHOISES = (
    ('created', 'Создана'),
    ('started', 'Запущена'),
    ('completed', 'Завершена'),
)


class Mailing(models.Model):
    """Модель таблицы - товары"""
    time = models.TimeField(verbose_name='Время рассылки')
    date = models.DateField(verbose_name='Дата рассылки')
    periodisity = models.CharField(max_length=20, choices=PERIODISITY_CHOISES, default='month',
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, default='created', verbose_name='Статус рассылки')
    client = models.ManyToManyField('Client', verbose_name='Клиент')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name='Пользователь')

    def __str__(self):
        return f'Дата - {self.date}: \n' \
               f'Сообщение - {self.message}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            (
                'set_status',
                'Can change status'
            )
        ]


class Client(models.Model):
    """Модель таблицы - товары"""
    email = models.EmailField(max_length=150, verbose_name='Контактная почта')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(max_length=500, blank=True, null=True, verbose_name='Коментарий')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Модель таблицы - товары"""
    subject = models.CharField(max_length=150, verbose_name='Тема письма')
    body = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Тело письма')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Log(models.Model):
    """Модель таблицы - товары"""
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время последеней попытки')
    status = models.BooleanField(verbose_name='Статус попытки')
    server_response = models.CharField(max_length=150, verbose_name='Ответ сервера', blank=True, null=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка', blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.time}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
