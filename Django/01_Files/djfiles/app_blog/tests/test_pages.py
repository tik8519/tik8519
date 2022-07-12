import datetime
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..urls import urlpatterns
from ..models import *
from ..views import *
from ..forms import *


class PagesTest(TestCase):
    def test_pages_urls(self):
        """Тестирует отклик страницы и соответствие шаблона"""
        pages_urls = [
            ('/', 'blog_list.html'),
            ('/blog_form/', 'blog_form.html'),
            ('/login/', 'users/login.html'),
            ('/register/', 'users/register.html'),
            ('/upload/', 'upload_blog.html')
        ]
        for url in pages_urls:
            response = self.client.get(url[0])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, url[1])


class TestBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create_user(username='Test')
        for blog in range(10):
            Blog.objects.create(
                author=Author(id=1),
                title='test_title',
                description='test_description'
            )
        # blog = Blog.objects.get(id=1)
        # print(blog.title)
        # тестовое заполнение базы данных

    def test_blog_number(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['blog_list']) == 10)
        # 'blog_list' это контекст передаваемый во Вьюхе тестируемого патерна.


class TestBlogForm(TestCase):
    def test_blog_form(self):
        date = datetime.date.today()
        form_blog = {
            'title': 'test_title',
            'description': 'test_description',
            'created_at': date
            }
        form = BlogForm(data=form_blog)
        self.assertTrue(form.is_valid())


class TestRegisterForm(TestCase):
    def test_user_form(self):
        date = datetime.date.today()
        user = {
            'username': 'test_name',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'rrr@mail.ru',
            'password1': 'televizor12',
            'password2': 'televizor12',
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
            'last_login': date,
            'date_joined': date
            }
        form = RegisterForm(data=user)
        # print(form.errors.as_json())  # указывает ошибки валидации
        self.assertTrue(form.is_valid())


class TestImageForms(TestCase):
    def test_image_form(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )  # имитирует файл с изображением
        # file = SimpleUploadedFile(name='test.jpg', content=open('app_blog/tests/test.jpg', 'rb').read(),
        #                           content_type='image/jpeg')
        file = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        # with open('app_blog/tests/test.jpg') as file:
        #     image = {'file_field': file,
        #              'blog_id': 1,
        #              }
        form = ImageForms({'file': file, 'blog_id': 1})
        print(form.errors.as_json())
        self.assertTrue(form.is_valid())
