from pathlib import Path
from django_cleanup.signals import cleanup_post_delete
from django.dispatch import receiver
from django.conf import settings
from authentication.models import UserProfile


@receiver(
    cleanup_post_delete,
    sender=UserProfile,
    dispatch_uid='delete-profile-image'
)
def delete_empty_folder(sender, **kwargs):
    """When django-cleanup delete image check if the image's folder
    is empty if it is delete the folder.
    """
    path = Path(settings.MEDIA_ROOT, kwargs['file_name']).parent
    if not next(path.iterdir(), None):
        path.rmdir()
