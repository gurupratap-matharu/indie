from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:product_id>/", views.cart_add, name="cart-add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart-remove"),
    path("", views.cart_detail, name="cart-detail"),
]
