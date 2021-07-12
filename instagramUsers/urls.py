from typing import Pattern
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlPatterns=[
    path('profile/', views.profile, name='profile'),
    path('', auth_views.LoginView.as_view(template_name='instagramUsers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='instagramUsers/logout.html'), name='logout'),
]