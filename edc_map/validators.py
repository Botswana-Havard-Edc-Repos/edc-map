from edc_map.site_mappers import site_mappers
from django.core.exceptions import ValidationError


def is_valid_map_area(value):
    """Validates the map_area string against a list of site_mappers map_areas."""
    if value.lower() not in [long.lower() for long in site_mappers.map_areas]:
        raise ValidationError(u'{0} is not a valid map_area.'.format(value))
