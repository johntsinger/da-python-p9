from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from utils.media import images_path


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        help_text='Required.')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username if self.username else self.email}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        default='images/userprofiles/default/profile_image.png',
        upload_to=images_path,
        verbose_name='Profile Image',
        blank=True,
    )

    @receiver(post_save, sender=User, dispatch_uid='create_user_profile')
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User, dispatch_uid='save_user_profile')
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'images/userprofiles/default/profile_image.png'
        super().save()

    def __str__(self):
        return self.user.username
