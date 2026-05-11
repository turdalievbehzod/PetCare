from django.urls import path

from apps.services.views import (
    FeaturedServiceListAPIView,
    ServiceCategoryListAPIView,
    ServiceCreateAPIView,
    ServiceDetailAPIView,
    ServiceListAPIView,
)

app_name = "services"

urlpatterns = [
    path("", ServiceListAPIView.as_view(), name="service-list"),
    path("featured/", FeaturedServiceListAPIView.as_view(), name="service-featured"),
    path("categories/", ServiceCategoryListAPIView.as_view(), name="service-category-list"),
    path("create/", ServiceCreateAPIView.as_view(), name="service-create"),
    path("<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
]
