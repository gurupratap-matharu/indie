from typing import ClassVar

from django.contrib import admin

from properties.models import Addon, Occurrence, Property, Room

admin.site.site_header = "Indie Cactus 🌵🏜️"
admin.site.site_title = "Indie Cactus Portal 🌵🏜️"
admin.site.index_title = "Welcome to Indie Cactus Admin Portal 🌵🏜️"


class RoomInline(admin.StackedInline):
    model = Room


class AddonInline(admin.TabularInline):
    model = Addon


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "property_type", "active")
    list_filter = ("property_type", "active")
    prepopulated_fields: ClassVar[dict] = {"slug": ("name",)}
    search_fields = ("name",)
    raw_id_fields = ("owner",)
    inlines: ClassVar[list] = [RoomInline, AddonInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "owner",
        )


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("room", "for_date", "rate", "availability")
    list_filter = ("for_date",)
    ordering = ("room", "for_date")
