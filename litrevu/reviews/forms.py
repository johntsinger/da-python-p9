from django import forms
from reviews.models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(forms.ModelForm):
    RATINGS = [
        (0, '0 stars'),
        (1, '1 stars'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

    rating = forms.ChoiceField(
        label='Rating',
        widget=forms.RadioSelect,
        choices=RATINGS,
        initial=0,
    )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')


class DeleteTicketForm(forms.Form):
    template_name = 'reviews/ticket_confirm_delete.html'
