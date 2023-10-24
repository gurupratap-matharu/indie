from django.urls import path

from . import views

app_name = "properties"


urlpatterns = [
    path("", views.PropertyListView.as_view(), name="property-list"),
    path("<slug:slug>/", views.PropertyDetailView.as_view(), name="property-detail"),
]
