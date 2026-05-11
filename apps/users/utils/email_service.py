import logging

import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def send_verification_email(to_email: str, code: str) -> bool:
    """Send a verification code via Resend API. Returns True on success."""
    resend.api_key = settings.RESEND_API_KEY

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "PetCare <noreply@petcare.com>")
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
        <h2 style="color: #2c7be5; margin-bottom: 8px;">PetCare</h2>
        <p style="color: #333; font-size: 15px;">Your email verification code:</p>
        <div style="background: #f4f6fa; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
            <span style="font-size: 36px; font-weight: bold; letter-spacing: 12px; color: #2c7be5;">{code}</span>
        </div>
        <p style="color: #666; font-size: 13px;">
            This code expires in <strong>5 minutes</strong>.<br>
            If you did not request this, please ignore this email.
        </p>
    </div>
    """
    try:
        params: resend.Emails.SendParams = {
            "from": from_email,
            "to": [to_email],
            "subject": "Your PetCare Verification Code",
            "html": html_body,
        }
        response = resend.Emails.send(params)
        email_id = response.get("id") if isinstance(response, dict) else getattr(response, "id", None)
        logger.info("Verification email sent to %s (id=%s)", to_email, email_id)
        return True
    except Exception as exc:
        logger.error("Failed to send verification email to %s: %s", to_email, exc)
        return False
