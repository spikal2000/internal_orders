from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
]
