from django.db import models

from apps.shared.models import BaseModel


class AboutPage(BaseModel):
    """Singleton-style model — keep only one active row."""
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_content = models.TextField()
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_content = models.TextField()
    commitment_title = models.CharField(
        max_length=200, default="We are committed for better service"
    )
    commitment_description = models.TextField(blank=True)
    stat1_value = models.PositiveIntegerField(default=0)
    stat1_label = models.CharField(max_length=100, default="Success Treatment")
    stat2_value = models.PositiveIntegerField(default=0)
    stat2_label = models.CharField(max_length=100, default="Happy Clients")
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"


class TeamMember(BaseModel):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    photo = models.ForeignKey(
        "shared.Media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members",
    )
    bio = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} — {self.title}"
