import logging

from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_verification_code(user_id, target_email=None):
    """
    Generate a fresh verification code and send it via email.
    target_email overrides user.email — used for the email-update flow
    where code must go to the new (unconfirmed) address.
    """
    from apps.users.models.users import User
    from apps.users.utils.email_service import send_verification_email

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning("send_verification_code: user %s not found", user_id)
        return

    code = user.generate_verification_code()
    email = target_email or user.email

    if getattr(settings, "DEBUG_EMAIL", False):
        logger.info("[DEBUG_EMAIL] code for %s: %s", email, code)
        print(f"[DEBUG_EMAIL] Verification code for {email}: {code}")
        return

    if email:
        sent = send_verification_email(email, code)
        if not sent:
            logger.error("Failed to send verification email to %s", email)
    else:
        logger.error("No email address for user %s — cannot send verification code", user_id)
