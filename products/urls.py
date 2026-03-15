from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_add, name='product_add'),
    path('<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('<int:product_id>/delete/', views.product_delete, name='product_delete'),

    # Units
    path('units', views.unit_list, name='unit_list'),
    path('units/<int:unit_id>/delete/', views.unit_delete, name='unit_delete'),
    path('units/add/', views.unit_add, name='unit_add'),

    # Branches
    path('branches', views.branch_list, name='branch_list'),
    path('branches/<int:branch_id>/delete/', views.branch_delete, name='branch_delete'),
    path('branches/add/', views.branch_add, name='branch_add'),

    # Categories
    path('categories', views.category_list, name='category_list'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    path('categories/add/', views.category_add, name='category_add'),
    
]