from abc import ABC

from rest_framework import serializers
from .models import *


class ClientSerializer(serializers.ModelSerializer):
    """Класс отображения в API модели с Клиентами"""

    class Meta:
        model = Client
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    """Класс отображения в API модели с Рассылками"""

    class Meta:
        model = Mailing
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """Класс отображения в API модели с Сообщениями"""

    class Meta:
        model = Message
        fields = '__all__'


class StatisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField()
    count = serializers.IntegerField()


class StatisticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.IntegerField()
    count = serializers.IntegerField()
