from .views import *
from django.urls import path


urlpatterns = [
    path('', personal_account, name='personal account'),
    path('shops/', show_shops, name='shops'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view),
    path('register/', register_view, name='register'),
]