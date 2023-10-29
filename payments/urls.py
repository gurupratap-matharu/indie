from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.PaymentView.as_view(), name="home"),
    path("success/", views.PaymentSuccessView.as_view(), name="success"),
    path("pending/", views.PaymentPendingView.as_view(), name="pending"),
    path("fail/", views.PaymentFailView.as_view(), name="fail"),
    path("mercadopago/success/", views.mercadopago_success, name="mercadopago-success"),
    path(
        "webhooks/mercadopago/", views.mercadopago_webhook, name="mercadopago-webhook"
    ),
]
