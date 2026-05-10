from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.about.models import AboutPage, TeamMember
from apps.about.serializers import (
    AboutPageSerializer,
    AboutPageWriteSerializer,
    TeamMemberSerializer,
    TeamMemberWriteSerializer,
)
from apps.shared.utils.custom_response import CustomResponse


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
