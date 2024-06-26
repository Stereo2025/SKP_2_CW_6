# Generated by Django 5.0.4 on 2024-04-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='slug')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Превью')),
                ('content', models.TextField(max_length=1000, verbose_name='Содержимое')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('views_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикации',
            },
        ),
    ]
