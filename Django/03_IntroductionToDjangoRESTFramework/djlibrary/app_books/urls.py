from django.urls import path
from .views import *

urlpatterns = [
    path('books/', BooksList.as_view(), name='books_list'),
    path('authors/', AuthorList2.as_view(), name='authors_list'),
]
