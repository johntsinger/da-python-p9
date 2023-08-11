from django.urls import path
from authentication import views as auth_views


urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('usermodifications/', auth_views.parameters_view, name='parameters'),
]
