from django.contrib import admin
from .models import *


class PublisherBlog(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'description', 'created_at']
    # список отображаемых в админке столбиков модели


class PublisherFile(admin.ModelAdmin):
    list_display = ['id', 'file', 'blog']


admin.site.register(Blog, PublisherBlog)  # регистрация модели в админке
admin.site.register(File, PublisherFile)
