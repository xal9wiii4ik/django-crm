import os

from django.contrib.auth.models import User
from django.db import models


def image_upload_path(instance, filename) -> os:
    """Функция для изменения пути сохранения файла"""

    return os.path.join(f'{instance.user.username}', filename)


class UserProfile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер Телефона', blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', blank=True)
    city = models.CharField(max_length=50, verbose_name='Город', blank=True)
    region = models.CharField(max_length=50, verbose_name='Область', blank=True)
    avatar = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}, {self.id}'
