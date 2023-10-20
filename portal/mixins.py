from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from properties.models import Property


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.reqeust.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerPropertyMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Property
    fields = ("name", "description", "property_type", "website")
    success_url = "/"  # <-- TODO: probably obj.get_absolute_url()


class OwnerPropertyEditMixin(OwnerPropertyMixin, OwnerEditMixin):
    template_name = "properties/property_update_form.html"
