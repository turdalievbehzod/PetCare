from rest_framework import serializers

from apps.blogs.models import Blog, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "uuid", "name", "slug"]


class BlogCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["name", "slug"]


class BlogListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    tag_list = serializers.ReadOnlyField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "uuid",
            "title",
            "slug",
            "excerpt",
            "cover_image_url",
            "author_name",
            "category",
            "tag_list",
            "views_count",
            "published_at",
            "created_at",
        ]

    def get_author_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or str(obj.author)
        return None

    def get_cover_image_url(self, obj):
        if obj.cover_image and obj.cover_image.file:
            request = self.context.get("request")
            url = obj.cover_image.file.url
            return request.build_absolute_uri(url) if request else url
        return None


class BlogDetailSerializer(BlogListSerializer):
    class Meta(BlogListSerializer.Meta):
        fields = BlogListSerializer.Meta.fields + ["content"]


class BlogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "slug",
            "excerpt",
            "content",
            "cover_image",
            "author",
            "category",
            "tags",
            "is_published",
            "published_at",
        ]
