# Generated by Django 5.0.4 on 2024-04-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default='', max_length=20, verbose_name='Код верификации'),
        ),
    ]
