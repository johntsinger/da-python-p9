from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default_profil_image.jpg',
        upload_to='images/profile',
        verbose_name='Profile Image',
    )

    def __str__(self):
        return self.user.username
