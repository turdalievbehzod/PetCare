import logging

from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.shared.utils.custom_response import CustomResponse
from apps.users.serializers.register import (
    LoginSerializer,
    MeSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    ResendVerificationCodeSerializer,
    SetPasswordSerializer,
    UpdateEmailSerializer,
    UpdatePasswordSerializer,
    VerifyCodeSerializer,
    VerifyUpdateEmailSerializer,
)
from apps.users.utils.verification_code import send_verification_code
from apps.users.views.users import UserSerializer

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────── Registration
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VALIDATION_ERROR",
            )

        user = serializer.save()

        data = {}
        if getattr(settings, "DEBUG_EMAIL", False):
            # Debug mode: generate code inline and include in response
            code = user.generate_verification_code()
            logger.info("[DEBUG_EMAIL] code for %s: %s", user.email, code)
            data["debug_code"] = code
        else:
            # Production: generate + send asynchronously via Celery
            send_verification_code(user.id)

        return CustomResponse.success(
            request=request,
            data=data or None,
            message_key="CODE_SENT_SUCCESSFULLY",
        )


# ──────────────────────────────────────────────────────────── Verify code
class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="CODE_VERIFICATION_ERROR",
            )

        user = serializer.validated_data["user"]
        data = {
            "user": UserSerializer(user).data,
            "tokens": user.get_tokens(),
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="CODE_VERIFIED_SUCCESSFULLY",
        )


# ────────────────────────────────────────────────────────── Resend code
class ResendVerificationCodeAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendVerificationCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="RESEND_CODE_ERROR",
            )

        user = serializer.validated_data["user"]

        if getattr(settings, "DEBUG_EMAIL", False):
            code = user.generate_verification_code()
            logger.info("[DEBUG_EMAIL] resend code for %s: %s", user.email, code)
        else:
            send_verification_code(user.id)

        return CustomResponse.success(
            request=request,
            message_key="CODE_SENT_SUCCESSFULLY",
        )


# ──────────────────────────────────────────────────────────────────── Login
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="LOGIN_ERROR",
            )

        user = serializer.validated_data["user"]
        data = {
            "user": UserSerializer(user).data,
            "tokens": user.get_tokens(),
        }

        return CustomResponse.success(
            request=request,
            data=data,
            message_key="LOGIN_SUCCESS",
        )


# ─────────────────────────────────────────────────── Password set (reset flow)
class SetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="SET_PASSWORD_ERROR",
            )

        serializer.save()

        return CustomResponse.success(
            request=request,
            message_key="PASSWORD_SET_SUCCESSFULLY",
        )


# ──────────────────────────────────────────────── Authenticated password change
class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="UPDATE_PASSWORD_ERROR",
            )

        serializer.save()

        return CustomResponse.success(
            request=request,
            message_key="PASSWORD_UPDATED_SUCCESSFULLY",
        )


# ─────────────────────────────────────────────────────────── Current user info
class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return CustomResponse.success(
            request=request,
            data=MeSerializer(request.user).data,
            message_key="USER_DATA_SUCCESS",
        )


# ──────────────────────────────────────── Email update — step 1: initiate
class UpdateEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="UPDATE_EMAIL_ERROR",
            )

        new_email = serializer.validated_data["email"]
        request.user.temp_email = new_email
        request.user.save(update_fields=["temp_email"])

        if getattr(settings, "DEBUG_EMAIL", False):
            code = request.user.generate_verification_code()
            logger.info("[DEBUG_EMAIL] email-update code for %s: %s", new_email, code)
        else:
            # Send code to the NEW (unconfirmed) address
            send_verification_code(request.user.id, target_email=new_email)

        return CustomResponse.success(
            request=request,
            message_key="EMAIL_UPDATE_CODE_SENT",
        )


# ─────────────────────────────────── Email update — step 2: verify and confirm
class VerifyUpdateEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyUpdateEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="VERIFY_UPDATE_EMAIL_ERROR",
            )

        user = serializer.validated_data["user"]
        user.email = user.temp_email
        user.temp_email = None
        user.save(update_fields=["email", "temp_email"])

        return CustomResponse.success(
            request=request,
            message_key="EMAIL_UPDATED_SUCCESSFULLY",
        )


# ───────────────────────────────────────────────────────── Profile update
class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def patch(self, request):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return CustomResponse.error(
                request=request,
                errors=serializer.errors,
                message_key="PROFILE_UPDATE_ERROR",
            )

        serializer.save()

        return CustomResponse.success(
            request=request,
            data=UserSerializer(request.user).data,
            message_key="PROFILE_UPDATED_SUCCESSFULLY",
        )
