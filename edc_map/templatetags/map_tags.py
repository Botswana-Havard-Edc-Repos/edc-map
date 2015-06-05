from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def use_gps_to_target_verification(self):
    verify = True
    if 'VERIFY_GPS' in dir(settings):
        verify = settings.VERIFY_GPS
    return verify
