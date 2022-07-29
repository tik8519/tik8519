from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import *


class CreatedClient(APIView):
    serializer_class = ClientSerializer

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        """Добавляет новую запись клиента"""
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """Обновляет запись клиента"""
        client_id = self.get_object(pk)
        serializer = ClientSerializer(client_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Удаляет запись клиента"""
        client_id = self.get_object(pk)
        client_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatedMailing(APIView):
    serializer_class = MailingSerializer

    def get_object(self, pk):
        try:
            return Mailing.objects.get(pk=pk)
        except Mailing.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        """Добавляет новую запись рассылки"""
        serializer = MailingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """Обновляет запись рассылки"""
        mailing_id = self.get_object(pk)
        serializer = MailingSerializer(mailing_id, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Удаляет запись рассылки"""
        mailing_id = self.get_object(pk)
        mailing_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatisticsMailing(generics.ListCreateAPIView):
    """Класс отображения детальной информации рассылки.
    Использовать /?filter=<int> для детальной информации по id рассылки"""
    serializer_class = StatisticsSerializer

    def get_queryset(self):
        try:
            item_name = self.request.query_params.get('filter')
            if item_name:
                queryset = Message.objects.raw(
                    f'SELECT id, status, COUNT(status) as count FROM app_mailing_message WHERE '
                    f'mailing_id = {item_name} GROUP BY status;')
            else:
                queryset = Message.objects.raw('SELECT id, status, COUNT(status) as count FROM app_mailing_message '
                                               'GROUP BY status;')
        except:
            return Response(MessageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return queryset


def sending(request):
    """Отправка рассылки в API"""
    if request.method == 'GET':
        return render(request, 'sending.html')
    elif request.method == 'POST':
        # токен правильно хранить в переменной окружения
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA0NTAzODQsImlzcyI6ImZhYnJpcXVlIiwibm' \
                'FtZSI6Ik1vemdvdm95RXZnZW5peSJ9.3v5MyCdBSc-oumiBCnHuoqIQXzH0Ibv2jUHCuO7FVPI'
        head = {'Authorization': token, "Content-type": "application/json"}
        queryset = Message.objects.raw('SELECT app_mailing_client.id as id, app_mailing_client.tel_number as '
                                       'tel_number, app_mailing_mailing.text as text FROM app_mailing_client JOIN '
                                       'app_mailing_message ON app_mailing_client.id = app_mailing_message.client_id '
                                       'JOIN app_mailing_mailing ON app_mailing_mailing.id = '
                                       'app_mailing_message.mailing_id WHERE app_mailing_message.status = 0')
        count = 0
        for item in queryset:
            url = f"https://probe.fbrq.cloud/v1/send/{item.id}"
            data = {"id": item.id, "phone": item.tel_number, "text": item.text}
            response = requests.post(url, headers=head, json=data)
            if response.status_code == 200:
                count += 1
                message_object = Message.objects.get(id=item.id)
                message_object.status = True
                message_object.save()
        if count == len(queryset):
            error_text = f'Cообщений доставлено: {count}'
        else:
            error_text = 'Сообщения не доставлены'
        return render(request, 'sending.html', {'error_text': error_text})
