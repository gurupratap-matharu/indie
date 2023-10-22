from django.urls import path

from .views import (
    DashboardView,
    ManagePropertyListView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyUpdateView,
)

app_name = "portal"

urlpatterns = [
    path("mine/", ManagePropertyListView.as_view(), name="manage_property_list"),
    path("create/", PropertyCreateView.as_view(), name="property_create"),
    path("<str:slug>/edit/", PropertyUpdateView.as_view(), name="property_update"),
    path("<str:slug>/delete/", PropertyDeleteView.as_view(), name="property_delete"),
    path("<str:slug>/", DashboardView.as_view(), name="dashboard"),
]
