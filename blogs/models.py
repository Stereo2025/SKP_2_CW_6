from django.conf import settings
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, blank=True, null=True, verbose_name='slug')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Превью')
    content = models.TextField(max_length=1000, verbose_name='Содержимое')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=1,
                             verbose_name='Пользователь', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
