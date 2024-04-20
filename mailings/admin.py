from django.contrib import admin

from mailings.models import Mailing, Message, Client, Log


# Register your models here.
@admin.register(Mailing)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'status')


@admin.register(Message)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')


@admin.register(Client)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name')


@admin.register(Log)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'status', 'server_response', 'mailing')
