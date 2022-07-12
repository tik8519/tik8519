from django.contrib.auth.models import User
from django.db import models


class Shops(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')


class Products(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    cost = models.IntegerField(verbose_name='cost')


class AvailabilityProducts(models.Model):
    name_shop = models.ForeignKey(Shops, unique=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, unique=False, on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='count')


class Basket(models.Model):
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, unique=False, on_delete=models.CASCADE)
    cost = models.IntegerField(verbose_name='cost')
    count = models.IntegerField(verbose_name='count')


class BuyHistory2(models.Model):
    product_id = models.IntegerField(verbose_name='product_id')
    name = models.CharField(max_length=100, db_index=True, verbose_name='name')
    count = models.IntegerField(verbose_name='count')
