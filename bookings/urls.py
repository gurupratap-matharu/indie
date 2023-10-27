from django.urls import path

from .views import BookingCreateView

app_name = "bookings"

urlpatterns = [
    path("create/", BookingCreateView.as_view(), name="booking-create"),
]
