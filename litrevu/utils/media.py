def images_path(instance, filename):
    """Get files path for media forlder"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    folder_name = instance.__class__.__name__.lower() + 's'
    if folder_name == 'userprofiles':
        return f'images/{folder_name}/users/user_{instance.user.id}/{filename}'
    return f'images/{folder_name}/users/user_{instance.user.id}/{filename}'
