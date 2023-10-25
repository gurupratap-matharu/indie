import logging

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .mixins import OwnerPropertyEditMixin, OwnerPropertyMixin

logger = logging.getLogger(__name__)


class ManagePropertyListView(OwnerPropertyMixin, ListView):
    template_name = "portal/manage_property_list.html"
    permission_required = "properties.view_property"


class DashboardView(OwnerPropertyMixin, DetailView):
    template_name = "portal/dashboard.html"
    permission_required = "properties.view_property"


class CalendarView(OwnerPropertyMixin, DetailView):
    template_name = "portal/calendar.html"
    permission_required = "properties.view_property"


class PropertyCreateView(OwnerPropertyEditMixin, CreateView):
    permission_required = "properties.add_property"
    template_name = "portal/property_create.html"


class PropertyUpdateView(OwnerPropertyEditMixin, UpdateView):
    permission_required = "properties.change_property"
    template_name = "portal/property_update.html"


class PropertyDeleteView(OwnerPropertyMixin, DeleteView):
    permission_required = "properties.delete_property"
    template_name = "portal/property_delete.html"
