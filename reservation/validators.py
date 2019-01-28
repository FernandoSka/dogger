from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

def actual_date_validator(value):
    if value < timezone.now():
        raise ValidationError(
            _('%(value)s is before than today'),
            params={'value': value},
        )
def hour_validator(value):
    if value < timedelta(hours = 1):
        raise ValidationError(
            _('the minimum hour is 1')
        )