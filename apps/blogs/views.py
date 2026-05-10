from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.blogs.models import Blog, BlogCategory
from apps.blogs.serializers import (
    BlogCategorySerializer,
    BlogCategoryWriteSerializer,
    BlogDetailSerializer,
    BlogListSerializer,
    BlogWriteSerializer,
)
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class BlogCategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = BlogCategory.objects.all()
        return CustomResponse.success(
            request=request,
            data=BlogCategorySerializer(categories, many=True).data,
            message_key="SUCCESS",
        )

    def post(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        serializer = BlogCategoryWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        category = serializer.save()
        return CustomResponse.success(
            request=request,
            data=BlogCategorySerializer(category).data,
            message_key="CREATED",
        )


class BlogListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Blog.objects.filter(is_published=True).select_related(
            "author", "category", "cover_image"
        )
        category_slug = request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        search = request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)

        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = BlogListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        serializer = BlogWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        blog = serializer.save()
        return CustomResponse.success(
            request=request,
            data=BlogDetailSerializer(blog, context={"request": request}).data,
            message_key="CREATED",
        )


class BlogDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def _get_object(self, slug):
        try:
            return Blog.objects.select_related(
                "author", "category", "cover_image"
            ).get(slug=slug, is_published=True)
        except Blog.DoesNotExist:
            return None

    def get(self, request, slug):
        blog = self._get_object(slug)
        if blog is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        Blog.objects.filter(pk=blog.pk).update(views_count=blog.views_count + 1)
        return CustomResponse.success(
            request=request,
            data=BlogDetailSerializer(blog, context={"request": request}).data,
            message_key="SUCCESS",
        )

    def patch(self, request, slug):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        blog = self._get_object(slug)
        if blog is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        serializer = BlogWriteSerializer(blog, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        blog = serializer.save()
        return CustomResponse.success(
            request=request,
            data=BlogDetailSerializer(blog, context={"request": request}).data,
            message_key="SUCCESS",
        )

    def delete(self, request, slug):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        blog = self._get_object(slug)
        if blog is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        blog.is_published = False
        blog.save(update_fields=["is_published", "updated_at"])
        return CustomResponse.success(request=request, message_key="SUCCESS")
