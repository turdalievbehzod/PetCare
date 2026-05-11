from django.contrib import admin

from apps.about.models import AboutPage, TeamMember, Testimonial


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ["mission_title", "stat1_value", "stat2_value", "years_experience", "appointments_count", "is_active", "updated_at"]
    list_editable = ["is_active"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
    fieldsets = [
        ("Mission", {"fields": ["mission_title", "mission_content"]}),
        ("Vision", {"fields": ["vision_title", "vision_content"]}),
        ("Commitment", {"fields": ["commitment_title", "commitment_description"]}),
        ("Stats", {"fields": [
            "stat1_value", "stat1_label",
            "stat2_value", "stat2_label",
            "years_experience",
            "appointments_count",
        ]}),
        ("Meta", {"fields": ["is_active", "uuid", "created_at", "updated_at"]}),
    ]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    search_fields = ["name", "title"]
    list_filter = ["is_active"]
    ordering = ["order"]
    raw_id_fields = ["photo"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "rating", "order", "is_active", "created_at"]
    list_editable = ["order", "is_active"]
    search_fields = ["name", "text"]
    list_filter = ["is_active", "rating"]
    ordering = ["order"]
    raw_id_fields = ["avatar"]
