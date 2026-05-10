from django.urls import path

from apps.blogs.views import BlogCategoryListAPIView, BlogDetailAPIView, BlogListAPIView

app_name = "blogs"

urlpatterns = [
    path("", BlogListAPIView.as_view(), name="blog-list"),
    path("categories/", BlogCategoryListAPIView.as_view(), name="category-list"),
    path("<slug:slug>/", BlogDetailAPIView.as_view(), name="blog-detail"),
]
