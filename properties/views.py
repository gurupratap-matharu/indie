import logging
from typing import Any

from django.views.generic import DetailView, ListView

from cart.forms import CartAddProductForm

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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cart_add_form"] = CartAddProductForm()
        return context
