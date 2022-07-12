from django.contrib import admin
from .models import *


class AdminAuthorInfo(admin.ModelAdmin):
    """класс отображения модели с Авторами в админке"""
    list_display = ['id', 'name', 'last_name', 'birth_year']
    # список отображаемых в админке столбиков модели


class AdminBooksInfo(admin.ModelAdmin):
    """класс отображения модели с Книгами в админке"""
    list_display = ['id', 'author', 'name', 'isbn', 'release_year', 'page_count']


admin.site.register(AuthorInfo, AdminAuthorInfo)  # регистрация модели в админке
admin.site.register(BooksInfo, AdminBooksInfo)