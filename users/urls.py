from django.urls import path
# from django.contrib.auth.views import *

from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
]
