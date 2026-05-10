from django.urls import path

from apps.about.views import AboutPageAPIView, TeamMemberDetailAPIView, TeamMemberListAPIView

app_name = "about"

urlpatterns = [
    path("", AboutPageAPIView.as_view(), name="about-page"),
    path("team/", TeamMemberListAPIView.as_view(), name="team-list"),
    path("team/<int:pk>/", TeamMemberDetailAPIView.as_view(), name="team-detail"),
]
