from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


class InvalidQuantityValidationError(ValidationError):
    default_detail = _('Invalid quantity for product.')
