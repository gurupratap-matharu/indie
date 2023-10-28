from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="home"),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("fail/", views.PaymentFailView.as_view(), name="fail"),
    path("mercadopago/success/", views.mercadopago_success, name="mercadopago_success"),
    path(
        "webhooks/mercadopago/", views.mercadopago_webhook, name="mercadopago_webhook"
    ),
]
