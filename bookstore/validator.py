from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

alphanumeric_with_space_validator = RegexValidator(r'^[0-9a-zA-Z\, _.-]*$',
                                                   _('Only alphanumeric & Space characters are allowed.'))
