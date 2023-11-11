import logging
from typing import Any

from django.db.models import CharField, F, Func, Value
from django.shortcuts import get_object_or_404
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


class ScheduleView(OwnerPropertyMixin, DetailView):
    """
    List view to show all rooms of the property from where detailed schedule can be linked.
    """

    template_name = "portal/schedule.html"
    permission_required = "properties.view_property"


class ScheduleDetailView(OwnerPropertyMixin, DetailView):
    """
    Show the schedule calendar for one single room.
    """

    template_name = "portal/schedule_detail.html"
    permission_required = "properties.view_property"

    def get_schedule_data(self, room):
        qs = room.occurrences.annotate(
            formatted_date=Func(
                F("for_date"),
                Value("yyyy-MM-dd hh:mm:ss"),
                function="to_char",
                output_field=CharField(),
            )
        )
        qs = qs.values_list("formatted_date", "availability")
        return list(qs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        qs = self.object.rooms.all()
        room_id = self.kwargs.get("room_id")

        context["room"] = room = get_object_or_404(qs, id=room_id)
        context["rates"] = self.get_schedule_data(room)

        return context


class PropertyCreateView(OwnerPropertyEditMixin, CreateView):
    permission_required = "properties.add_property"
    template_name = "portal/property_create.html"


class PropertyUpdateView(OwnerPropertyEditMixin, UpdateView):
    permission_required = "properties.change_property"
    template_name = "portal/property_update.html"


class PropertyDeleteView(OwnerPropertyMixin, DeleteView):
    permission_required = "properties.delete_property"
    template_name = "portal/property_delete.html"
