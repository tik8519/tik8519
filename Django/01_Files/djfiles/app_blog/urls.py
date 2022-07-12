from django.conf import settings
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static


urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('<int:pk>', BlogDetailView.as_view(), name='blog-detail'),
    path('blog_form/', BlogFormView.as_view()),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view),
    path('register/', register_view, name='register'),
    path('edit/', UserEditFormView.as_view()),
    path('upload/', upload_blog, name='upload'),
    # path('user_info/', users_info, name='user_info')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
