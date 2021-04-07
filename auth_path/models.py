from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Uid(models.Model):
    """Model uid for future verification of user"""

    uid = models.CharField(max_length=25)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.uid = urlsafe_base64_encode(force_bytes(self.user.id))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uid}, {self.user.username}'
