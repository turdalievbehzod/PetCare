from django.contrib import admin

from apps.blogs.models import Blog, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "author", "is_published", "views_count", "published_at"]
    list_editable = ["is_published"]
    list_filter = ["is_published", "category"]
    search_fields = ["title", "excerpt", "content"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["cover_image", "author"]
    date_hierarchy = "published_at"
    readonly_fields = ["uuid", "views_count", "created_at", "updated_at"]
    fieldsets = [
        ("Content", {"fields": ["title", "slug", "excerpt", "content"]}),
        ("Media & Relations", {"fields": ["cover_image", "author", "category", "tags"]}),
        ("Publishing", {"fields": ["is_published", "published_at"]}),
        ("Meta", {"fields": ["uuid", "views_count", "created_at", "updated_at"]}),
    ]
