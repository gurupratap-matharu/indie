from django.contrib import admin

from properties.models import Property

admin.site.site_header = "Indie Cactus 🌵🏜️"
admin.site.site_title = "Indie Cactus Portal 🌵🏜️"
admin.site.index_title = "Welcome to Indie Cactus Admin Portal 🌵🏜️"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "property_type")
    list_filter = ("property_type",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    raw_id_fields = ("owner",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("owner")
