import logging

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .mixins import OwnerPropertyEditMixin, OwnerPropertyMixin

logger = logging.getLogger(__name__)


class PortalHomeView(OwnerPropertyMixin, TemplateView):
    template_name = "portal/home.html"
    permission_required = "properties.view_property"


class ManagePropertyListView(OwnerPropertyMixin, ListView):
    template_name = "portal/manage_property_list.html"
    permission_required = "properties.view_property"


class PropertyCreateView(OwnerPropertyEditMixin, CreateView):
    permission_required = "properties.add_property"


class PropertyUpdateView(OwnerPropertyEditMixin, UpdateView):
    permission_required = "properties.change_property"


class PropertyDeleteView(OwnerPropertyMixin, DeleteView):
    permission_required = "properties.delete_property"
    template_name = "portal/property_delete.html"
