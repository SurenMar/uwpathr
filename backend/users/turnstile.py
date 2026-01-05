import requests
from typing import Optional
from django.conf import settings
from django.core.cache import cache

TURNSTILE_VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'


class CaptchaVerificationError(Exception):
    """Raised when Turnstile verification fails."""


def get_remote_ip(request) -> Optional[str]:
    """Best-effort client IP extraction for passing to Turnstile."""
    if not request:
        return None

    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()

    return (
        request.META.get('HTTP_CF_CONNECTING_IP')
        or request.META.get('REMOTE_ADDR')
        or None
    )


def verify_turnstile_token(token: str, remote_ip: Optional[str] = None) -> dict:
    if not token:
        raise CaptchaVerificationError('CAPTCHA token is missing.')

    secret = getattr(settings, 'TURNSTILE_SECRET_KEY', None)
    if not secret:
        raise CaptchaVerificationError('CAPTCHA secret key is not configured.')

    cache_key = f'turnstile:used:{token}'
    if cache.get(cache_key):
        raise CaptchaVerificationError('CAPTCHA token was already used.')

    payload = {'secret': secret, 'response': token}
    if remote_ip:
        payload['remoteip'] = remote_ip

    try:
        response = requests.post(
            TURNSTILE_VERIFY_URL,
            data=payload,
            timeout=getattr(settings, 'TURNSTILE_VERIFY_TIMEOUT', 5),
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise CaptchaVerificationError('CAPTCHA verification could not reach Cloudflare.') from exc
    except ValueError as exc:
        raise CaptchaVerificationError('CAPTCHA verification response was invalid.') from exc

    if not data.get('success'):
        raise CaptchaVerificationError('CAPTCHA validation failed.')

    cache.set(
        cache_key,
        True,
        timeout=getattr(settings, 'TURNSTILE_REPLAY_CACHE_SECONDS', 600),
    )

    return data
