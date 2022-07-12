from django.db import models


class AuthorInfo(models.Model):
    """модель с данными Авторов"""
    name = models.CharField(max_length=100, verbose_name='Имя автора')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия автора')
    birth_year = models.DateField(auto_now=False, verbose_name='Год рождения')

    def __str__(self):  # при отображении в шаблоне показывает не объект, а выбранную колонку
        return self.name


class BooksInfo(models.Model):
    """модель с данными Книг"""
    author = models.ForeignKey(AuthorInfo, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200, verbose_name='название')
    isbn = models.CharField(max_length=13, verbose_name='isbn')
    release_year = models.DateField(auto_now=False, verbose_name='год публикации')
    page_count = models.IntegerField(verbose_name='количество страниц')
