from django.urls import path

from apps.contact.views import ContactInfoAPIView, ContactInquiryAPIView

app_name = "contact"

urlpatterns = [
    path("", ContactInquiryAPIView.as_view(), name="inquiry"),
    path("info/", ContactInfoAPIView.as_view(), name="info"),
]
