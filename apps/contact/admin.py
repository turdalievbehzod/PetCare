from django.contrib import admin

from apps.contact.models import ContactInfo, ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "is_read", "created_at"]
    list_editable = ["is_read"]
    list_filter = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["phone", "email", "address", "is_active", "updated_at"]
    list_editable = ["is_active"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
