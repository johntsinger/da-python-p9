from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import InlineRadios
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

    def __init__(self, *args, **kwargs):
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
                Div(
                    HTML(
                        """
                        <a class="btn btn-secondary w-100"
                        href="{% url 'feed' %}"
                        role="button">Return</a>
                        """
                    ),
                    css_class="col-md-6 pe-md-3"
                ),
                Div(
                    Submit(
                        'submit',
                        'Send',
                        css_class="btn btn-primary w-100"
                    ),
                    css_class="col-md-6 ps-md-3"
                ),
                css_class="vstack gap-4 gap-md-0 my-4 py-4 d-flex flex-column flex-md-row"
            )
        )


class DeleteTicketForm(forms.Form):
    template_name = 'reviews/ticket_confirm_delete.html'


class SubscriptionFrom(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ('followed_user',)

