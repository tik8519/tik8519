from rest_framework import serializers
from .models import *


class BooksSerializer(serializers.ModelSerializer):
    """класс отображения в API модели с Книгами"""

    class Meta:
        model = BooksInfo
        fields = ['id', 'name', 'isbn', 'release_year', 'page_count', 'author']


class AuthorSerializer(serializers.ModelSerializer):
    """класс отображения в API модели с Авторами"""

    class Meta:
        model = AuthorInfo
        fields = ['id', 'name', 'last_name', 'birth_year']
