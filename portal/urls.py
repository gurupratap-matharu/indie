from django.urls import include, path

from .views import (
    DashboardView,
    ManagePropertyListView,
    PropertyCreateView,
    PropertyDeleteView,
    PropertyUpdateView,
)

app_name = "portal"

portal_patterns = [
    # These are urlpatterns specific to a property
    path("edit/", PropertyUpdateView.as_view(), name="property-update"),
    path("delete/", PropertyDeleteView.as_view(), name="property-delete"),
    path("", DashboardView.as_view(), name="dashboard"),
]

urlpatterns = [
    path("mine/", ManagePropertyListView.as_view(), name="manage-property-list"),
    path("create/", PropertyCreateView.as_view(), name="property-create"),
    path("<str:slug>/", include(portal_patterns)),
]
