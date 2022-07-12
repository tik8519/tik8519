from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Author(User):
    """Наследник класс User в котором по умолчанию сохраняются данные авторизованных пользователей (требуется импорт)"""

    def __str__(self):
        return f'{self.username}'

    class Meta:
        proxy = True
        ordering = ('first_name',)


class Blog(models.Model):
    author = models.ForeignKey('Author', blank=True, default=None, null=True, on_delete=models.CASCADE,
                               related_name=_('author'), verbose_name=_('author'))
    title = models.CharField(max_length=100, db_index=True, verbose_name=_('title'))
    description = models.CharField(max_length=1000, default='', verbose_name=_('description'))
    created_at = models.DateTimeField(auto_created=True, default=timezone.now, verbose_name=_('publication date'))

    def __str__(self):
        return f'{self.title}'

    def reduced_text(self):
        """Позволяет создать новый атрибут у класса и использовать его в админке или страничке.
        Можно изменять или комбинировать существующие данные модели"""
        if len(self.description) > 100:
            return self.description[:100] + '...'
        else:
            return self.description

    class Meta:
        ordering = ['-created_at', ]  # имя во множественном числе
        verbose_name = _('blog')  # имя в единичном числе
        verbose_name_plural = _('blogs')  # имя во множественном числе


class File(models.Model):
    file = models.ImageField(upload_to='image/', blank=True, verbose_name=_('file'))
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name=_('blog'), verbose_name=_('blog'))

    class Meta:
        verbose_name = _('file')  # имя в единичном числе
        verbose_name_plural = _('files')  # имя во множественном числе
