import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    """Год не может быть больше текущего."""
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Год указан больше текущего года {current_year}')
