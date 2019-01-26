from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def min_validator(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is less than 0'),
            params={'value': value},
        )

def rate_validator(value):
    if value < 0 or value > 5:
        raise ValidationError(
            _('%(value)s is out of range'),
            params={'value': value},
        )

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')