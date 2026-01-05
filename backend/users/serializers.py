from typing import Any, Dict
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import UserAccount
from .turnstile import (
    CaptchaVerificationError,
    get_remote_ip,
    verify_turnstile_token,
)


class CaptchaUserCreateSerializer(BaseUserCreateSerializer):
    captcha_token = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = UserAccount
        fields = (
            'id',
            'email',
            'first_name',
            'start_year',
            'password',
            're_password',
            'captcha_token',
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        token = attrs.pop('captcha_token', None)
        request = self.context.get('request')
        remote_ip = get_remote_ip(request)

        try:
            verify_turnstile_token(token, remote_ip=remote_ip)
        except CaptchaVerificationError as exc:
            raise serializers.ValidationError({'captcha': str(exc)})

        return super().validate(attrs)
