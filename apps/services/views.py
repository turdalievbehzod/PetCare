from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.services.models import Service
from apps.services.serializers import ServiceSerializer, ServiceWriteSerializer
from apps.shared.utils.custom_response import CustomResponse


class ServiceListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        services = Service.objects.filter(is_active=True)
        serializer = ServiceSerializer(services, many=True)
        return CustomResponse.success(
            request=request,
            data=serializer.data,
            message_key="SUCCESS",
        )


class ServiceCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ServiceWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        service = serializer.save()
        return CustomResponse.success(
            request=request,
            data=ServiceSerializer(service).data,
            message_key="CREATED",
        )


class ServiceDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def _get_object(self, pk):
        try:
            return Service.objects.get(pk=pk, is_active=True)
        except Service.DoesNotExist:
            return None

    def get(self, request, pk):
        service = self._get_object(pk)
        if service is None:
            return CustomResponse.error(
                request=request,
                message_key="NOT_FOUND",
            )
        return CustomResponse.success(
            request=request,
            data=ServiceSerializer(service).data,
            message_key="SUCCESS",
        )

    def patch(self, request, pk):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        service = self._get_object(pk)
        if service is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        serializer = ServiceWriteSerializer(service, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        service = serializer.save()
        return CustomResponse.success(
            request=request,
            data=ServiceSerializer(service).data,
            message_key="SUCCESS",
        )

    def delete(self, request, pk):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        service = self._get_object(pk)
        if service is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        service.is_active = False
        service.save(update_fields=["is_active", "updated_at"])
        return CustomResponse.success(request=request, message_key="SUCCESS")
