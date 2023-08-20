from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from authentication.models import UserProfile, User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
    )


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class ImageChangeForm(forms.ModelForm):
    change_image = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
    )
    image = forms.ImageField(
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = ('image',)


class MyPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
    )


class UsernameChangeForm(forms.Form):
    change_username = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True,
    )
    current_username = forms.CharField(
        disabled=True,
        required=False,
    )
    new_username = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_username(self):
        username = self.cleaned_data['new_username']
        if User.objects.exclude(
            pk=self.user.id
        ).filter(
            username=username
        ).exists():
            raise forms.ValidationError(
                f'Username {username} is already in use.')
        return username


class EmailChangeForm(forms.Form):
    change_email = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True,
    )
    current_email = forms.EmailField(
        disabled=True,
        required=False,
    )
    new_email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        email = self.cleaned_data['new_email']
        if User.objects.exclude(
            pk=self.user.id
        ).filter(
            email=email
        ).exists():
            raise forms.ValidationError(
                f'email {email} is already in use.')
        return email


class DeleteAccountForm(forms.Form):
    delete_account = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True,
    )
    username = forms.CharField(
        max_length=63)
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput
    )
    template_name = "authentication/delete_account_form.html"
