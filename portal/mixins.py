import logging

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from properties.models import Property

logger = logging.getLogger(__name__)


class OwnerMixin:
    def get_queryset(self):
        logger.info("🔎 filtering qs for %s", self.request.user)
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        logger.info("📝 form valid so assigning owner as %s", self.request.user)
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerPropertyMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Property
    fields = ("name", "description", "property_type", "website")
    success_url = "/"  # <-- TODO: probably obj.get_absolute_url()
    # success_url = reverse_lazy("portal:manage-property-list")


class OwnerPropertyEditMixin(OwnerPropertyMixin, OwnerEditMixin):
    template_name = "properties/property_update_form.html"
