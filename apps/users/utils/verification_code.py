import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_verification_code(user_id):
    from apps.users.models.users import User
    from apps.users.utils.eskiz import send_sms

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning("send_verification_code: user %s not found", user_id)
        return

    code = user.generate_verification_code()

    if getattr(settings, 'DEBUG_SMS', False):
        logger.info("[DEBUG_SMS] code for %s: %s", user.phone_number or user.email, code)
        print(f"[DEBUG_SMS] Verification code for {user.phone_number or user.email}: {code}")
        return

    if user.phone_number:
        message = f"Your verification code: {code}"
        sent = send_sms(user.phone_number, message)
        if not sent:
            logger.error("Failed to send verification SMS to %s", user.phone_number)
    elif user.email:
        # Email fallback placeholder — wire up an email backend when ready
        logger.info("Email verification code %s for %s", code, user.email)
    else:
        logger.error("No contact info for user %s to send verification code", user_id)
