from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class BooksListPagination(PageNumberPagination):
    """кастомная пагинация для классов"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20


# class BooksList2(generics.ListCreateAPIView):
#     # к этому классу подключилась кастомная пагинация
#     queryset = BooksInfo.objects.all()
#     serializer_class = BooksSerializer
#     pagination_class = BooksListPagination


class AuthorList2(generics.ListCreateAPIView):
    """класс отображения сериализованой модели с Авторами в API"""
    # к этому классу подключилась пагинация по умолчанию
    # queryset = AuthorInfo.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        """фильтрация данных в зависимости от параметра в URL-ссылке"""
        # для получения данных по фильтру необходима ссылка: http://127.0.0.1:8000/authors/?name=имя_автора
        queryset = AuthorInfo.objects.all()
        item_name = self.request.query_params.get('name')
        if item_name:
            queryset = AuthorInfo.objects.filter(name=item_name)
        return queryset


class BooksList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """класс отображения сериализованой модели с Книгами в API"""
    # к этому классу подключилась кастомная пагинация
    pagination_class = BooksListPagination
    serializer_class = BooksSerializer

    def get_queryset(self):
        """фильтрация данных в зависимости от параметра в URL-ссылке"""
        # для получения данных по фильтру необходима ссылка: http://127.0.0.1:8000/authors/?name=имя_автора
        queryset = BooksInfo.objects.all()
        item_name = self.request.query_params.get('name')
        item_author = self.request.query_params.get('author')
        item_min = self.request.query_params.get('min')
        item_max = self.request.query_params.get('max')
        item_equally = self.request.query_params.get('equally')
        if item_name and item_author:
            queryset = BooksInfo.objects.filter(name=item_name, author=item_author)
        elif item_min:
            queryset = BooksInfo.objects.filter(page_count__gt=item_min)  # параметр __gt выбирает значения больше
        elif item_max:
            queryset = BooksInfo.objects.filter(page_count__lt=item_max)  # параметр __lt выбирает значения меньше
        elif item_equally:
            queryset = BooksInfo.objects.filter(page_count=item_equally)
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# class AuthorList(APIView):
#     def get(self, request):
#         authors = AuthorInfo.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return Response(serializer.data)
