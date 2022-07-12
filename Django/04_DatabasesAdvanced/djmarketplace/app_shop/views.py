from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db import connection, reset_queries
import logging
import datetime


logger = logging.getLogger(__name__)


def register_view(request):
    """Регистрация"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


class Login(LoginView):
    """Вход в личный кабинет"""
    template_name = 'users/login.html'

    def form_valid(self, form):
        logger.info(f'{datetime.datetime.now()} Пользователь {form.get_user()} авторизовался')
        return super().form_valid(form)


def logout_view(request):
    """Выход из личного кабинета"""
    logout(request)
    response = redirect('/')
    return response


def user_account(request):
    """Отображение информации в личном кабинете"""
    user = request.user  # достаточно одного запроса к объекту user
    if user.is_authenticated:
        user_id = user.id
        # user = User.objects.only('id', 'username').get(id=user_id)
        # дублирующий запрос
        user_statys = user.profile.statys()
        basket_count = Basket.objects.filter(user_id=user_id).count()
        # обработка данных о наличие в магазинах товаров и запаковка в словарь для передачи в представление:
        product = {}
        # availability_products = AvailabilityProducts.objects.all() # старый запрос
        availability_products = AvailabilityProducts.objects.select_related().all()  # оптимизированный запрос
        for i_product in availability_products:
            if i_product.count > 0:
                product_info = (i_product.product.name, i_product.product.cost, i_product.count,
                                i_product.name_shop_id, i_product.product_id)
                # product_shop_id = (i_product.name_shop.id, i_product.product.id)
                if i_product.name_shop.name in product.keys():
                    product[i_product.name_shop.name].append(product_info)
                else:
                    product[i_product.name_shop.name] = [product_info]
        return render(request, 'user_account.html', {'user': user, 'user_statys': user_statys, 'product': product,
                                                     'basket_count': basket_count})
    else:
        return render(request, 'user_account.html')


def balance(request):
    """Пополнение баланса счета"""
    if request.method == 'GET':
        return render(request, 'users/balance.html')
    elif request.method == 'POST':
        refill = request.POST['refill']
        try:
            refill = int(refill)
            error_text = f'Успешно зачислено балов: {refill}'
            user_id = request.user.id
            # for p in User.objects.raw('SELECT id FROM auth_user WHERE id = {user_id}'.format(user_id=user_id)):
            #     p.profile.balance += refill
            #     p.profile.save()
            # работают оба варианта
            p = User.objects.raw('SELECT id FROM auth_user WHERE id = {user_id}'.format(user_id=user_id))
            p[0].profile.balance += refill
            p[0].profile.save()
            logger.info(f'{datetime.datetime.now()} Пользователь {request.user} пополнил баланс')
        except ValueError:
            error_text = 'Ошибка! Введите целое число!'
        return render(request, 'users/balance.html', {'error_text': error_text})


def add_basket(request):
    """Обрабатывает запрос по кнопке "купить", определяет id магазина, товара и количество"""
    answer = '<h3>Ошибка! Введите целое число!</h3>'
    try:
        count = int(request.POST['count'])  # количество товара передаваемое через кнопку "купить"
        shop_id = request.POST['shop_id']
        product_id = request.POST['product_id']
        product = AvailabilityProducts.objects.get(name_shop_id=shop_id, product_id=product_id)
        if product.count < count:
            answer = '<h3>Ошибка! Вы указали не доступное количество!</h3>'
            raise ValueError()
        else:
            product.count -= count
            product.save()
            # product_name = Products.objects.get(id=product_id)  # старый запрос
            product_name = product.product  # новый запрос
            user = request.user
            order = Basket(user=user, product=product_name, cost=product_name.cost, count=count)
            order.save()
            logger.info(f'{datetime.datetime.now()} Пользователь {request.user} оформил заказ')
    except ValueError:
        return HttpResponse(answer)
    # print(connection.queries, '\nВсего:', len(connection.queries))  # количество запросов SQL
    return redirect('/')


def basket(request):
    """Отображение товаров в корзине"""
    user_id = request.user.id
    # basket_product = Basket.objects.filter(user_id=user_id) старый запрос
    basket_product = Basket.objects.select_related().filter(user_id=user_id)  # оптимизированный запрос
    sum = 0
    for product in basket_product:
        sum += product.count * product.cost
    # print(connection.queries, '\nВсего:', len(connection.queries))  # количество запросов SQL
    return render(request, 'basket.html', {'basket_product': basket_product, 'sum': sum})


def buy(request):
    """Логика работы после нажатия кнопки купить в корзине"""
    logger.info(f'{datetime.datetime.now()} Пользователь {request.user} оплатил заказ')
    user = request.user
    user_id = user.id
    basket_product = Basket.objects.select_related().filter(user_id=user_id)
    summ = 0
    for product in basket_product:
        summ += product.count * product.cost
    if summ > user.profile.balance:
        return HttpResponse('<h3>Не достаточно средств на счете</h3><h3><a href="/balance/">Пополнить баланс</a></h3>')
    else:
        # для оптимизации использовать bulk_update
        for product in basket_product:
            history_product = BuyHistory2()
            history_product.product_id = product.product.id
            history_product.name = product.product.name
            history_product.count = product.count
            history_product.save()
            product.delete()
        first_statys = user.profile.statys()
        request.user.profile.balance -= summ
        request.user.profile.purchases += summ
        request.user.profile.save()
        second_statys = user.profile.statys()
        if first_statys != second_statys:
            logger.info(f'{datetime.datetime.now()} Пользователь {request.user} повысил свой статут')
        # print(connection.queries, '\nВсего:', len(connection.queries))  # количество запросов SQL
        return redirect('/')


def top_product(request):
    logger.info('Пользователь открыл статистику продаж')
    top_products = BuyHistory2.objects.raw \
        ('SELECT DISTINCT id, name, SUM(count) as total_count FROM app_shop_buyhistory2'
         ' GROUP BY name ORDER BY total_count DESC;')
    # в SQL запрос обязательно включать id иначе django выдает ошибку
    print(connection.queries, '\nВсего:', len(connection.queries))  # количество запросов SQL
    return render(request, 'top_product.html', {'top_products': top_products})
