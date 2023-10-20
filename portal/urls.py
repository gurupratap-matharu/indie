from django.urls import path

from .views import (
    ManagePropertyListView,
    PortalHomeView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyUpdateView,
)

app_name = "portal"

urlpatterns = [
    path("", PortalHomeView.as_view(), name="home"),
    path("mine/", ManagePropertyListView.as_view(), name="manage_propery_list"),
    path("create/", PropertyCreateView.as_view(), name="property_create"),
    path("<uuid:id>/edit/", PropertyUpdateView.as_view(), name="property_update"),
    path("<uuid:id>/delete/", PropertyDeleteView.as_view(), name="property_delete"),
]
