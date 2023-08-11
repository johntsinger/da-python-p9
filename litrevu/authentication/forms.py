from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from authentication.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label='Username'
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput,
        label='Password'
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image',)


class MyPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(
        widget=forms.HiddenInput,
        initial=True
    )


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


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput
    )
    template_name = "authentication/delete_account_form.html"
