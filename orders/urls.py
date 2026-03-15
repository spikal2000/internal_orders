from django.urls import path
from . import views

app_name = 'orders' 

urlpatterns = [
    path("shop/", views.order_shop, name="order_shop"),
    path("", views.order_list, name="order_list"),
    path("<int:order_id>/mark-read/", views.order_mark_read, name="order_mark_read"),
]

