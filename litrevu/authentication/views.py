from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from authentication.forms import (
    LoginForm, SignupForm, MyPasswordChangeForm, EmailChangeForm,
    DeleteAccountForm, ImageChangeForm
)
from authentication.models import UserProfile


def login_view(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            messages.error(request, 'Invalid username or password')
    return render(
        request,
        'authentication/login.html',
        context={'form': form}
    )


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    user_form = SignupForm()
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # auto login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        'authentication/signup.html',
        context={
            'user_form': user_form,
        }
    )


@login_required
def parameters_view(request):
    if request.method == "POST":
        if 'change_password' in request.POST:
            password_form = MyPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # update_session_auth_hash otherwise the user’s auth session
                # will be invalidated and she/he will have to log in again.
                update_session_auth_hash(request, user)
                messages.success(
                    request,
                    'Your password was successfully updated !'
                )
                return redirect('parameters')
            else:
                image_form = ImageChangeForm(
                    instance=request.user.userprofile
                )
                email_form = EmailChangeForm(
                    initial={'current_email': request.user.email}
                )
                delete_form = DeleteAccountForm()

        if 'change_email' in request.POST:
            email_form = EmailChangeForm(
                request.POST,
                initial={'current_email': request.user.email}
            )
            if email_form.is_valid():
                user = request.user
                user.email = email_form.cleaned_data['new_email']
                user.save()
                messages.success(
                    request,
                    'Your email was successfully updated !'
                )
                return redirect('parameters')
            else:
                image_form = ImageChangeForm(
                    instance=request.user.userprofile
                )
                password_form = MyPasswordChangeForm(request.user)
                delete_form = DeleteAccountForm()

        if 'change_image' in request.POST:
            image_form = ImageChangeForm(
                request.POST,
                request.FILES,
                instance=request.user.userprofile
            )
            if image_form.is_valid():
                image_form.save()
                messages.success(
                    request,
                    'Your profile image was successfully updated !'
                )
                return redirect('parameters')
            else:
                email_form = EmailChangeForm(
                    initial={'current_email': request.user.email}
                )
                password_form = MyPasswordChangeForm(request.user)
                delete_form = DeleteAccountForm()

        if 'delete_account' in request.POST:
            delete_form = DeleteAccountForm(request.POST)
            if delete_form.is_valid():
                user = authenticate(
                    username=delete_form.cleaned_data['username'],
                    password=delete_form.cleaned_data['password'],
                )
                if user is not None:
                    request.user.delete()
                    return redirect('/')
                else:
                    return redirect('parameters')
    else:
        image_form = ImageChangeForm(instance=request.user.userprofile)
        password_form = MyPasswordChangeForm(request.user)
        email_form = EmailChangeForm(
            initial={'current_email': request.user.email})
        delete_form = DeleteAccountForm()
    return render(
        request,
        'authentication/parameters.html',
        context={
            'password_form': password_form,
            'email_form': email_form,
            'delete_form': delete_form,
            'image_form': image_form,
        },
    )
