from django.urls import path

from apps.services.views import ServiceCreateAPIView, ServiceDetailAPIView, ServiceListAPIView

app_name = "services"

urlpatterns = [
    path("", ServiceListAPIView.as_view(), name="service-list"),
    path("create/", ServiceCreateAPIView.as_view(), name="service-create"),
    path("<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
]
