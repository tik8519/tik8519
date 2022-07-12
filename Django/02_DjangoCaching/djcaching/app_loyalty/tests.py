from django.test import TestCase
from .models import *


class PagesTest(TestCase):
    def test_pages_urls(self):
        """Тестирует отклик страницы и соответствие шаблона"""
        pages_urls = [
            ('/', 'main.html'),
            ('/shops/', 'shops.html'),
            ('/login/', 'users/login.html'),
            ('/register/', 'users/register.html')
        ]
        for url in pages_urls:
            response = self.client.get(url[0])
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, url[1])


class TestShops(TestCase):
    @classmethod
    def setUpTestData(cls):
        for blog in range(10):
            Shops.objects.create(
                name='test_name',
                address='test_address'
            )
        # тестовое заполнение базы данных

    def test_shops_number(self):
        response = self.client.get('/shops/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['shops']) == 10)
        # 'shops' это контекст передаваемый во Вьюхе тестируемого патерна.
