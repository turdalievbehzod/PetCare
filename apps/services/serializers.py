from rest_framework import serializers

from apps.services.models import Service, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["id", "name", "slug"]


class ServiceSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", default=None, read_only=True)
    category_slug = serializers.CharField(source="category.slug", default=None, read_only=True)

    class Meta:
        model = Service
        fields = [
            "id", "uuid", "slug", "title", "description", "icon_class",
            "image_url", "category_name", "category_slug",
            "is_featured", "order", "created_at",
        ]

    def get_image_url(self, obj):
        if obj.image and obj.image.file:
            request = self.context.get("request")
            url = obj.image.file.url
            return request.build_absolute_uri(url) if request else url
        return None


class ServiceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["title", "slug", "description", "icon_class", "image", "category", "is_featured", "order", "is_active"]
