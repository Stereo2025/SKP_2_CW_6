from django.contrib import admin

from blogs.models import Blog


# Register your models here.
@admin.register(Blog)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_added')
