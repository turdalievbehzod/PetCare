from django.contrib import admin

from apps.services.models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "icon_class", "is_featured", "order", "is_active", "created_at"]
    list_editable = ["is_featured", "order", "is_active"]
    search_fields = ["title", "description", "slug"]
    list_filter = ["is_active", "is_featured", "category"]
    ordering = ["order"]
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ("title",)}
