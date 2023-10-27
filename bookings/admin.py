from django.contrib import admin

from .models import Booking, BookingItem


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    raw_id_fields = ("product",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "residence",
        "paid",
        "created",
    )
    list_filter = ("paid", "created")
    inlines = (BookingItemInline,)
