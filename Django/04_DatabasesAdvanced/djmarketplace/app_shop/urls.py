from django.urls import path
from .views import *


urlpatterns = [
    path('', user_account, name='blog'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view),
    path('register/', register_view, name='register'),
    path('balance/', balance, name='balance'),
    path('add_basket/', add_basket, name='add_basket'),
    path('basket/', basket, name='basket'),
    path('basket/buy/', buy, name='buy'),
    path('top_product/', top_product, name='top_product'),
]
