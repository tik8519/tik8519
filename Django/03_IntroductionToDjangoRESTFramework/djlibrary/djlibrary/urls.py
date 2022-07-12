"""djlibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# создание автоматической генерации документации для передачи стороннему разработчику для интеграции
# необходимо прописать в urls
schema_view = get_schema_view(
    openapi.Info(
        title="Item API",
        default_version='v1',
        description='Описание проекта',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.ru"),
        license=openapi.License(name=''),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),  # включение документации в админке должен быть в верху
    path('admin/', admin.site.urls),
    path('', include('app_books.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger")
]
