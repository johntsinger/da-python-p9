from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        default='images/profile/default/profile_image.png',
        upload_to='images/profile/user',
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
            self.image = 'images/profile/default/profile_image.png'
        super().save()

    def __str__(self):
        return self.user.username
