from django.contrib import admin

from apps.services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "icon_class", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    search_fields = ["title", "description"]
    list_filter = ["is_active"]
    ordering = ["order"]
