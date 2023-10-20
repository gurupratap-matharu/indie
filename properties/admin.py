from typing import ClassVar

from django.contrib import admin

from properties.models import Property, Room

admin.site.site_header = "Indie Cactus 🌵🏜️"
admin.site.site_title = "Indie Cactus Portal 🌵🏜️"
admin.site.index_title = "Welcome to Indie Cactus Admin Portal 🌵🏜️"


class RoomInline(admin.StackedInline):
    model = Room


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "property_type")
    list_filter = ("property_type",)
    prepopulated_fields: ClassVar[dict] = {"slug": ("name",)}
    search_fields = ("name",)
    raw_id_fields = ("owner",)
    inlines: ClassVar[list] = [RoomInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("owner")
