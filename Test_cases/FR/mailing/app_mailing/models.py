from datetime import timedelta
from django.db import models
from django.utils import timezone


class Client(models.Model):
    """Сущность 'клиент'"""
    tel_number = models.IntegerField(verbose_name='telephone number')
    code = models.IntegerField(verbose_name='code')
    tag = models.CharField(max_length=30, db_index=True, verbose_name='tag')
    time_zone = models.CharField(max_length=10, verbose_name='time zone')


class Mailing(models.Model):
    """Сущность 'рассылка'"""
    date_start = models.DateTimeField(auto_created=True, default=timezone.now, verbose_name='date start')
    text = models.TextField(verbose_name='text')
    code = models.IntegerField(verbose_name='code')
    tag = models.CharField(max_length=30, db_index=True, verbose_name='tag')
    date_stop = models.DateTimeField(auto_created=True, default=timezone.now() + timedelta(days=1),
                                     verbose_name='date stop')


class Message(models.Model):
    """Сущность 'сообщение'"""
    date_creation = models.DateTimeField(auto_created=True, default=timezone.now, verbose_name='date creation')
    status = models.BooleanField(verbose_name='status')
    client = models.ForeignKey('Client', blank=True, default=None, null=True, on_delete=models.SET_NULL,
                               related_name='client', verbose_name='client')
    mailing = models.ForeignKey('Mailing', blank=True, default=None, null=True, on_delete=models.SET_NULL,
                                related_name='mailing', verbose_name='mailing')
