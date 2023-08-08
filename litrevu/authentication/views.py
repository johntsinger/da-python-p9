from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from authentication.forms import LoginForm, SignupForm


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
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        'authentication/signup.html',
        context={'form': form}
    )
