from django.db import models

from apps.shared.models import BaseModel


class Service(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        default="flaticon-animal-kingdom",
        help_text="Flaticon CSS class, e.g. flaticon-animal-kingdom",
    )
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title
