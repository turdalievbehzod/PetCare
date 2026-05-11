from django.db import models
from django.utils.text import slugify

from apps.shared.models import BaseModel


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, null=True, blank=True)
    description = models.TextField()
    icon_class = models.CharField(
        max_length=100,
        default="flaticon-animal-kingdom",
        help_text="Flaticon CSS class, e.g. flaticon-animal-kingdom",
    )
    image = models.ForeignKey(
        "shared.Media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_images",
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services",
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
