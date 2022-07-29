from django.urls import path
from .views import *

urlpatterns = [
    path('client/created/', CreatedClient.as_view(), name='client_created'),
    path('client/delete/<int:pk>/', CreatedClient.as_view(), name='client_delete'),
    path('client/put/<int:pk>/', CreatedClient.as_view(), name='client_put'),
    path('mailing/created/', CreatedMailing.as_view(), name='mailing_created'),
    path('mailing/delete/<int:pk>/', CreatedMailing.as_view(), name='mailing_delete'),
    path('mailing/put/<int:pk>/', CreatedMailing.as_view(), name='mailing_put'),
    path('statistics/', StatisticsMailing.as_view(), name='statistics_detailed'),
    path('sending/', sending, name='sending'),
]
