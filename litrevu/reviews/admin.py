from django.contrib import admin
from reviews.models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    ordering = ('user',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'ticket', 'rating')
    ordering = ('user',)


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    ordering = ('user',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowAdmin)
