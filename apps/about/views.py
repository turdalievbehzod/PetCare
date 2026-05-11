from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.about.models import AboutPage, TeamMember, Testimonial
from apps.about.serializers import (
    AboutPageSerializer,
    AboutPageWriteSerializer,
    TeamMemberSerializer,
    TeamMemberWriteSerializer,
    TestimonialSerializer,
    TestimonialWriteSerializer,
)
from apps.shared.utils.custom_response import CustomResponse


class AboutStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = AboutPage.objects.filter(is_active=True).first()
        veterinarians = TeamMember.objects.filter(is_active=True).count()

        data = {
            "successful_treatments": page.stat1_value if page else 0,
            "successful_treatments_label": page.stat1_label if page else "Successful Treatments",
            "happy_clients": page.stat2_value if page else 0,
            "happy_clients_label": page.stat2_label if page else "Happy Clients",
            "veterinarians": veterinarians,
            "years_experience": page.years_experience if page else 0,
            "appointments_count": page.appointments_count if page else 0,
        }
        return CustomResponse.success(request=request, data=data, message_key="SUCCESS")


class AboutPageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = AboutPage.objects.filter(is_active=True).first()
        if page is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        return CustomResponse.success(
            request=request,
            data=AboutPageSerializer(page).data,
            message_key="SUCCESS",
        )

    def put(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        page = AboutPage.objects.filter(is_active=True).first()
        if page is None:
            serializer = AboutPageWriteSerializer(data=request.data)
        else:
            serializer = AboutPageWriteSerializer(page, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        page = serializer.save()
        return CustomResponse.success(
            request=request,
            data=AboutPageSerializer(page).data,
            message_key="SUCCESS",
        )


class TeamMemberListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        members = TeamMember.objects.filter(is_active=True)
        serializer = TeamMemberSerializer(members, many=True, context={"request": request})
        return CustomResponse.success(
            request=request,
            data=serializer.data,
            message_key="SUCCESS",
        )

    def post(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        serializer = TeamMemberWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        member = serializer.save()
        return CustomResponse.success(
            request=request,
            data=TeamMemberSerializer(member, context={"request": request}).data,
            message_key="CREATED",
        )


class TeamMemberDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def _get_object(self, pk):
        try:
            return TeamMember.objects.get(pk=pk, is_active=True)
        except TeamMember.DoesNotExist:
            return None

    def get(self, request, pk):
        member = self._get_object(pk)
        if member is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        return CustomResponse.success(
            request=request,
            data=TeamMemberSerializer(member, context={"request": request}).data,
            message_key="SUCCESS",
        )

    def patch(self, request, pk):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        member = self._get_object(pk)
        if member is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        serializer = TeamMemberWriteSerializer(member, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        member = serializer.save()
        return CustomResponse.success(
            request=request,
            data=TeamMemberSerializer(member, context={"request": request}).data,
            message_key="SUCCESS",
        )

    def delete(self, request, pk):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        member = self._get_object(pk)
        if member is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        member.is_active = False
        member.save(update_fields=["is_active", "updated_at"])
        return CustomResponse.success(request=request, message_key="SUCCESS")


class TestimonialListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        testimonials = Testimonial.objects.filter(is_active=True)
        serializer = TestimonialSerializer(testimonials, many=True, context={"request": request})
        return CustomResponse.success(
            request=request,
            data=serializer.data,
            message_key="SUCCESS",
        )

    def post(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        serializer = TestimonialWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        testimonial = serializer.save()
        return CustomResponse.success(
            request=request,
            data=TestimonialSerializer(testimonial, context={"request": request}).data,
            message_key="CREATED",
        )
