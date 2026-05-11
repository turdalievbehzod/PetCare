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


class BlogNavItemSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["id", "title", "slug", "cover_image_url"]

    def get_cover_image_url(self, obj):
        if obj.cover_image and obj.cover_image.file:
            request = self.context.get("request")
            url = obj.cover_image.file.url
            return request.build_absolute_uri(url) if request else url
        return None


class BlogListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    tag_list = serializers.ReadOnlyField()
    read_time = serializers.SerializerMethodField()

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
            "read_time",
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

    def get_read_time(self, obj):
        if not obj.content:
            return 1
        return max(1, round(len(obj.content.split()) / 200))


class BlogDetailSerializer(BlogListSerializer):
    related_posts = serializers.SerializerMethodField()
    previous_post = serializers.SerializerMethodField()
    next_post = serializers.SerializerMethodField()

    class Meta(BlogListSerializer.Meta):
        fields = BlogListSerializer.Meta.fields + [
            "content",
            "related_posts",
            "previous_post",
            "next_post",
        ]

    def get_related_posts(self, obj):
        if not obj.category_id:
            return []
        qs = (
            Blog.objects.filter(is_published=True, category_id=obj.category_id)
            .exclude(pk=obj.pk)
            .select_related("author", "category", "cover_image")[:4]
        )
        return BlogListSerializer(qs, many=True, context=self.context).data

    def get_previous_post(self, obj):
        prev = (
            Blog.objects.filter(is_published=True, created_at__lt=obj.created_at)
            .order_by("-created_at")
            .select_related("cover_image")
            .first()
        )
        return BlogNavItemSerializer(prev, context=self.context).data if prev else None

    def get_next_post(self, obj):
        nxt = (
            Blog.objects.filter(is_published=True, created_at__gt=obj.created_at)
            .order_by("created_at")
            .select_related("cover_image")
            .first()
        )
        return BlogNavItemSerializer(nxt, context=self.context).data if nxt else None


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
