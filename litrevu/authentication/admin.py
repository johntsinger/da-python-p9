from django.contrib import admin
from authentication.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')


admin.site.register(User, MyUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
