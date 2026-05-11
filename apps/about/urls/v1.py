from django.urls import path

from apps.about.views import (
    AboutPageAPIView,
    AboutStatsAPIView,
    TeamMemberDetailAPIView,
    TeamMemberListAPIView,
    TestimonialListAPIView,
)

app_name = "about"

urlpatterns = [
    path("", AboutPageAPIView.as_view(), name="about-page"),
    path("stats/", AboutStatsAPIView.as_view(), name="about-stats"),
    path("team/", TeamMemberListAPIView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamMemberDetailAPIView.as_view(), name="team-detail"),
    path("testimonials/", TestimonialListAPIView.as_view(), name="testimonial-list"),
]
