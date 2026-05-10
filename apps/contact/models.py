from django.db import models

from apps.shared.models import BaseModel


class ContactInquiry(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} — {self.subject}"


class ContactInfo(BaseModel):
    """Singleton-style model — keep only one active row."""
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    working_hours = models.CharField(max_length=100, default="Mon to Fri 9am to 6pm")
    map_embed_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def __str__(self):
        return f"Contact Info — {self.phone}"
