from django.urls import path

from apps.blogs.views import BlogCategoryListAPIView, BlogDetailAPIView, BlogListAPIView, BlogTagListAPIView

app_name = "blogs"

urlpatterns = [
    path("", BlogListAPIView.as_view(), name="blog-list"),
    path("categories/", BlogCategoryListAPIView.as_view(), name="category-list"),
    path("tags/", BlogTagListAPIView.as_view(), name="tag-list"),
    path("<slug:slug>/", BlogDetailAPIView.as_view(), name="blog-detail"),
]
