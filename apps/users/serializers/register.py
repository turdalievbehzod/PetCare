from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.models import Language
from apps.users.models.users import User, VerificationCode
from apps.users.utils.generate_password import generate_password

_RESEND_COOLDOWN = getattr(settings, "VERIFICATION_CODE_RESEND_COOLDOWN", 60)
_MAX_ATTEMPTS = getattr(settings, "VERIFICATION_CODE_MAX_ATTEMPTS", 5)


# ──────────────────────────────────────────────────────────────── Registration
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    language = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "language", "password", "confirm_password"]

    def validate_email(self, email):
        email = email.strip().lower()
        if User.objects.filter(email=email).exists():
            raise CustomException(message_key="EMAIL_EXIST_ERROR")
        return email

    def validate_language(self, language):
        if language not in Language.values:
            raise CustomException(message_key="INVALID_LANGUAGE_TYPE")
        return language

    def validate_password(self, value):
        if len(value) < 6:
            raise CustomException(message_key="PASSWORD_TOO_SHORT")
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise CustomException(message_key="PASSWORDS_DO_NOT_MATCH")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user


# ──────────────────────────────────────────────────────────── Verify code
class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email", "").strip().lower()
        code = attrs.get("code", "").strip()

        user = User.objects.filter(email=email).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")

        verification = VerificationCode.objects.filter(user=user).first()
        if not verification:
            raise CustomException(message_key="INVALID_VERIFICATION_CODE")

        # Expiration check
        expires_at = verification.created_at + timedelta(
            seconds=verification.expiration_seconds
        )
        if timezone.now() > expires_at:
            verification.delete()
            raise CustomException(message_key="VERIFICATION_CODE_EXPIRED")

        # Brute-force protection
        if verification.attempts >= _MAX_ATTEMPTS:
            verification.delete()
            raise CustomException(message_key="MAX_VERIFICATION_ATTEMPTS")

        # Wrong code → increment attempts and persist
        if verification.code != code:
            verification.attempts += 1
            verification.save(update_fields=["attempts"])
            raise CustomException(message_key="INVALID_VERIFICATION_CODE")

        verification.delete()

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        attrs["user"] = user
        return attrs


# ──────────────────────────────────────────────────────────────────── Login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")

        if not user.check_password(password):
            raise CustomException(message_key="INVALID_CREDENTIALS")

        if not user.is_active:
            raise CustomException(message_key="USER_NOT_VERIFIED")

        attrs["user"] = user
        return attrs


# ────────────────────────────────────────────────────────── Resend code
class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"].strip().lower()

        user = User.objects.filter(email=email).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")

        # Cooldown: reject if a code was sent less than RESEND_COOLDOWN seconds ago
        recent = VerificationCode.objects.filter(user=user).first()
        if recent:
            elapsed = (timezone.now() - recent.created_at).total_seconds()
            if elapsed < _RESEND_COOLDOWN:
                raise CustomException(message_key="RESEND_CODE_COOLDOWN")

        attrs["user"] = user
        return attrs


# ─────────────────────────────────────────────────── Password reset / set
class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise CustomException(message_key="PASSWORDS_DO_NOT_MATCH")

        user = User.objects.filter(email=attrs["email"].strip().lower()).first()
        if not user:
            raise CustomException(message_key="USER_NOT_FOUND")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password1"])
        user.save()
        return user


# ──────────────────────────────────────────────── Authenticated password change
class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.check_password(attrs["old_password"]):
            raise CustomException(message_key="INVALID_OLD_PASSWORD")

        if attrs["new_password1"] != attrs["new_password2"]:
            raise CustomException(message_key="PASSWORDS_DO_NOT_MATCH")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password1"])
        user.save()
        return user


# ─────────────────────────────────────────────────────────── Me (read-only)
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
            "language",
        ]


# ─────────────────────────────────────────── Email update (step 1 — initiate)
class UpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs["email"].strip().lower()

        if User.objects.filter(email=email).exists():
            raise CustomException(message_key="EMAIL_EXIST_ERROR")

        attrs["email"] = email
        return attrs


# ─────────────────────── Email update (step 2 — confirm code sent to new email)
class VerifyUpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        email = attrs["email"].strip().lower()

        if email != (user.temp_email or "").strip().lower():
            raise CustomException(message_key="INVALID_EMAIL")

        verification = VerificationCode.objects.filter(user=user).first()
        if not verification:
            raise CustomException(message_key="INVALID_VERIFICATION_CODE")

        expires_at = verification.created_at + timedelta(
            seconds=verification.expiration_seconds
        )
        if timezone.now() > expires_at:
            verification.delete()
            raise CustomException(message_key="VERIFICATION_CODE_EXPIRED")

        if verification.attempts >= _MAX_ATTEMPTS:
            verification.delete()
            raise CustomException(message_key="MAX_VERIFICATION_ATTEMPTS")

        if verification.code != attrs["code"].strip():
            verification.attempts += 1
            verification.save(update_fields=["attempts"])
            raise CustomException(message_key="INVALID_VERIFICATION_CODE")

        verification.delete()
        attrs["user"] = user
        return attrs


# ───────────────────────────────────────────────────────── Profile update
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "language",
        ]
