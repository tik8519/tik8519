from django.contrib.auth.models import User
from django.db import models


class Person(User):
    """Наследник класс User в котором по умолчанию сохраняются данные авторизованных пользователей (требуется импорт)"""

    balance = models.IntegerField(auto_created=False, default=0, verbose_name='balance')

    def __str__(self):
        return f'{self.username}'


class Shops(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    address = models.CharField(max_length=100, db_index=True, verbose_name='address')


class Products(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    cost = models.IntegerField(verbose_name='cost')


class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Products, unique=False, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='count')


class Stocks(models.Model):
    name = models.CharField(max_length=1000, db_index=True, verbose_name='name')
