from django.contrib import admin

from .models import Order


@admin.register(Order)
class ClientAdmin(admin.ModelAdmin):
    shown_fields = ("order_id", "price", "delivery_date")
    ids_fields = ("own_id",)

    list_display = ids_fields + shown_fields
    list_editable = shown_fields
    list_display_links = ids_fields
    search_fields = ids_fields + shown_fields
    list_filter = ids_fields + shown_fields

    empty_value_display = "-пусто-"
