from django.contrib import admin
from .models import *


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'tel_number', 'code', 'tag', 'time_zone']  # список отображаемых в админке столбиков модели
    list_filter = ['code', 'tag', 'time_zone']  # список для фильтрации в админке


class MailingAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_start', 'text', 'code', 'tag', 'date_stop']
    list_filter = ['date_start', 'code', 'tag', 'date_stop']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_creation', 'status', 'client', 'mailing']
    list_filter = ['date_creation', 'status', 'client', 'mailing']


admin.site.register(Client, ClientAdmin)  # регистрация модели в админке
admin.site.register(Mailing, MailingAdmin)
admin.site.register(Message, MessageAdmin)
