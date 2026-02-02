"""
URL configuration for accounts app
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('bank/', views.bank_info, name='bank_info'),
]
