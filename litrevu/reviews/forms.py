from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import InlineRadios
from django import forms
from reviews.models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Media:
        js = (
            'reviews/js/change_image.js',
        )

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

    def __init__(self, *args, **kwargs):
        """Add FormHelper to make RadioSelect inline"""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('headline'),
            InlineRadios(
                'rating',
                css_class=(
                    "my-2 gap-4 gap-md-0"
                    " d-flex justify-content-between flex-wrap"
                )
            ),
            Field('body'),
            Div(
                HTML(
                    "{% include 'reviews/submit_buttons_form.html' %}"
                )
            )
        )


class DeleteTicketForm(forms.Form):
    template_name = 'reviews/ticket_confirm_delete.html'


class SubscriptionFrom(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ('followed_user',)
