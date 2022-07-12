from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppBlogConfig(AppConfig):
    name = 'app_blog'
    verbose_name = _("Blog")
    # дает возможность делать интернализацию названия приложения в админке
