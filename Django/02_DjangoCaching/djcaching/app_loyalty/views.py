import random

from django.contrib.auth.views import LoginView

from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.cache import *


class Login(LoginView):
    template_name = 'users/login.html'


def personal_account(request):
    user_name = request.user.username  # дальше используется для кеширования
    purchases = []
    shopping_list = PurchaseHistory.objects.filter(user_id=request.user.id)
    for position in shopping_list:
        for title in Products.objects.filter(id=position.id):
            summ = title.cost * position.count
            purchases.append({'name': title.name, 'cost': title.cost, 'count': position.count, 'summ': summ})
    if len(Person.objects.all()) != 0:
        balance = Person.objects.get(id=request.user.id)
    else:
        balance = 0
    promotion_cache_key = 'promotion:{}'.format(user_name)  # уникальный ключ кеширования
    purchases_cache_key = 'purchases:{}'.format(user_name)
    len_stock = len(Stocks.objects.all())
    if len_stock > 0:
        random_promotion = random.randint(1, len_stock)
        promotion = Stocks.objects.get(id=random_promotion)
    else:
        promotion = 'Нет акций'
    user_account_cache_data = {
        promotion_cache_key: promotion,
        purchases_cache_key: purchases
    }  # словарь для кеширования
    cache.set_many(user_account_cache_data)  # кеширование нескольких объектов
    # cache.get_or_set(promotion_cache_key, promotion, 30*60)  # кеширует одиночный объект на время в секундах
    return render(request, 'main.html', {'purchases': purchases, 'promotion': promotion, 'balance': balance})


def register_view(request):
    """Функция регистрации"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # по-хорошему при регистрации должен генерироваться список покупок
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def show_shops(request):
    shops = Shops.objects.all()
    return render(request, 'shops.html', {'shops': shops})


def logout_view(request):
    logout(request)
    response = redirect('/')  # перенаправляет на главную страницу
    return response
