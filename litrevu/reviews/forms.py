from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit
from crispy_forms.bootstrap import InlineRadios, FieldWithButtons
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from reviews.models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Media:
        js = (
            'js/change_image.js',
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
                    "{% include 'reviews/includes/submit_buttons_form.html' %}"
                )
            )
        )


class DeleteTicketForm(forms.Form):
    template_name = 'reviews/ticket_confirm_delete.html'


class SubscriptionFrom(forms.ModelForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'placeholder':
                    'Enter the username of the user you wish to follow'
            }
        ),
    )

    class Meta:
        model = UserFollows
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        if kwargs.get('request'):
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons(
                'username',
                Submit(
                    'submit',
                    'Follow'
                ),
                input_size="input-group-sm",
            )
        )

    def clean_username(self):
        User = get_user_model()
        try:
            followed_user = User.objects.get(
                username=self.cleaned_data['username']
            )
        except User.DoesNotExist:
            messages.error(
                self.request,
                'This user does not exist'
            )
            raise ValidationError('This user does not exist')
        else:
            if followed_user == self.request.user:
                messages.error(
                    self.request,
                    "You can't follow yourself !"
                )
                raise ValidationError("You can't follow yourself !")
            elif followed_user.id in self.request.user.following.values_list(
                'followed_user',
                flat=True
            ):
                messages.error(
                    self.request,
                    f'You are already following {followed_user}')
                raise ValidationError(
                    f'You are already following {followed_user}'
                )

        return followed_user
