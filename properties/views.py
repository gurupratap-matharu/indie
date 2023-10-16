import logging

from django.views.generic import DetailView, ListView

from .models import Property

logger = logging.getLogger(__name__)


class PropertyListView(ListView):
    model = Property
    context_object_name = "properties"
    template_name = "properties/property_list.html"


class PropertyDetailView(DetailView):
    model = Property
    context_object_name = "property"
    template_name = "properties/property_detail.html"
