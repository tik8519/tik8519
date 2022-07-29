from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Документация Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Item API",
        default_version='v1',
        description='Описание проекта',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tik85@mail.ru"),
        license=openapi.License(name='Open'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('app_mailing.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger"),
]
