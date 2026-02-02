"""
URL configuration for designs app
"""
from django.urls import path
from . import views

app_name = 'designs'

urlpatterns = [
    path('', views.design_list, name='list'),
    path('upload/', views.design_upload, name='upload'),
    path('<uuid:pk>/', views.design_detail, name='detail'),
    path('<uuid:pk>/approve/', views.design_approve, name='approve'),
    path('<uuid:pk>/reject/', views.design_reject, name='reject'),
    path('<uuid:pk>/delete/', views.design_delete, name='delete'),
]

