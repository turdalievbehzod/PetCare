import logging

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

ESKIZ_BASE_URL = "https://notify.eskiz.uz/api"
ESKIZ_TOKEN_CACHE_KEY = "eskiz_auth_token"
# Cache for 28 days — Eskiz tokens expire in 30 days
ESKIZ_TOKEN_TTL = 28 * 24 * 3600


def _fetch_token() -> str:
    response = requests.post(
        f"{ESKIZ_BASE_URL}/auth/login",
        data={"email": settings.ESKIZ_EMAIL, "password": settings.ESKIZ_PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    token = response.json()["data"]["token"]
    cache.set(ESKIZ_TOKEN_CACHE_KEY, token, timeout=ESKIZ_TOKEN_TTL)
    return token


def _get_token() -> str:
    token = cache.get(ESKIZ_TOKEN_CACHE_KEY)
    return token if token else _fetch_token()


def send_sms(phone_number: str, message: str) -> bool:
    """Send SMS via Eskiz gateway. Returns True on success."""
    phone = phone_number.lstrip("+")
    try:
        token = _get_token()
        response = requests.post(
            f"{ESKIZ_BASE_URL}/message/sms/send",
            headers={"Authorization": f"Bearer {token}"},
            data={"mobile_phone": phone, "message": message, "from": "4546"},
            timeout=10,
        )
        if response.status_code == 401:
            # Token expired — force refresh and retry once
            cache.delete(ESKIZ_TOKEN_CACHE_KEY)
            token = _fetch_token()
            response = requests.post(
                f"{ESKIZ_BASE_URL}/message/sms/send",
                headers={"Authorization": f"Bearer {token}"},
                data={"mobile_phone": phone, "message": message, "from": "4546"},
                timeout=10,
            )
        response.raise_for_status()
        return True
    except Exception as exc:
        logger.error("Eskiz SMS send failed to %s: %s", phone_number, exc)
        return False
