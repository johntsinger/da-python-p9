from django.contrib import admin
from reviews.models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
admin.site.register(UserFollows)
