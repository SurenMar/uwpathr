from djoser.email import ActivationEmail as DjoserActivationEmail
from django.conf import settings

class ActivationEmail(DjoserActivationEmail):
    def get_from_email(self):
        return settings.DEFAULT_FROM_EMAIL
