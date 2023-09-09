from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from reviews.models import Ticket, Review, UserFollows


class UserFollowsAdminForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = '__all__'

    def clean(self):
        """Clean and validate fields that depend on each other,
        if user == followed_user or UserFollows already exists
        raise ValidationError.
        """
        if all(key in self.cleaned_data for key in ('user', 'followed_user')):
            if self.cleaned_data['user'] == self.cleaned_data['followed_user']:
                raise ValidationError("A user can't follow himself.")
            if UserFollows.objects.filter(
                user=self.cleaned_data['user'],
                followed_user=self.cleaned_data['followed_user']
            ).first():
                raise ValidationError(
                    (
                        f"User {self.cleaned_data['user']} already "
                        f"follows {self.cleaned_data['followed_user']}."
                    )
                )
        return self.cleaned_data


class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

    def clean_ticket(self):
        """Clean ticket field, if review already has a ticket
        raise ValidationError.
        """
        if Ticket.objects.get(
            pk=self.cleaned_data['ticket'].pk
        ).review_set.first():
            raise ValidationError('This ticket has already a review.')
        return self.cleaned_data['ticket']


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    ordering = ('user',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'ticket', 'rating')
    ordering = ('user',)
    form = ReviewAdminForm


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
    ordering = ('user',)
    form = UserFollowsAdminForm


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowAdmin)
