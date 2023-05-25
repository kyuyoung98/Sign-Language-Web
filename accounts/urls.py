from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('answer/', views.chat_list, name='chat_list'),
    path('answer/chat/', views.chat, name='chat'),
]