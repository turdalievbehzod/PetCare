from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from apps.contact.models import ContactInfo, ContactInquiry
from apps.contact.serializers import ContactInfoSerializer, ContactInquirySerializer
from apps.shared.utils.custom_response import CustomResponse


class ContactInquiryAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactInquirySerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        serializer.save()
        return CustomResponse.success(
            request=request,
            message_key="CONTACT_INQUIRY_SENT",
        )


class ContactInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        info = ContactInfo.objects.filter(is_active=True).first()
        if info is None:
            return CustomResponse.error(request=request, message_key="NOT_FOUND")
        return CustomResponse.success(
            request=request,
            data=ContactInfoSerializer(info).data,
            message_key="SUCCESS",
        )

    def put(self, request):
        if not request.user.is_staff:
            return CustomResponse.error(request=request, message_key="PERMISSION_DENIED")
        info = ContactInfo.objects.filter(is_active=True).first()
        if info is None:
            serializer = ContactInfoSerializer(data=request.data)
        else:
            serializer = ContactInfoSerializer(info, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )
        info = serializer.save()
        return CustomResponse.success(
            request=request,
            data=ContactInfoSerializer(info).data,
            message_key="SUCCESS",
        )
