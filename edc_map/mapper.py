import sys

from geopy import Point

from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.core.management.color import color_style

from .geo_mixin import GeoMixin

LANDMARK_NAME = 0
LATITUDE = 2
LETTERS = list(map(chr, range(65, 91)))
LONGITUDE = 1

style = color_style()


class Mapper(GeoMixin):

    center_lat = None
    center_lon = None
    landmarks = None  # format ((name, longitude, latitude), )
    map_area = None
    radius = 5.5
    mapper_model = None

    def __init__(self):
        self.name = self.map_area or f'mapper {self.__class__.__name__}'
        app_config = django_apps.get_app_config('edc_map')
        mapper_model = self.mapper_model or app_config.mapper_model
        if not mapper_model:
            raise ImproperlyConfigured(
                f'Invalid mapper_model. Got None. See {repr(self)}.')
        try:
            self.item_model = django_apps.get_model(*mapper_model.split('.'))
        except LookupError as e:
            sys.stdout.write(style.WARNING(
                f'\n  Warning. Lookup error in mapper. See {repr(self)}. Got {e} '
                'edc_map.apps.AppConfig\n'))
        else:
            self.item_model_cls = self.item_model
            self.item_label = self.item_model._meta.verbose_name
        self.load()

    def __repr__(self):
        return 'Mapper({0.map_area!r})'.format(self)

    def __str__(self):
        return '({0.map_area!r})'.format(self)

    def load(self):
        return None

    @property
    def __dict__(self):
        return {
            'map_area': self.map_area,
            'center_lat': self.center_lat,
            'center_lon': self.center_lon,
            'radius': self.radius}

    @property
    def area_center_point(self):
        return Point(self.center_lat, self.center_lon)

    @property
    def area_radius(self):
        return self.radius

    def point_in_map_area(self, point):
        """Return True if point is within mapper area radius."""
        return self.point_in_radius(
            point, self.area_center_point, self.area_radius)

    def raise_if_not_in_map_area(self, point):
        self.raise_if_not_in_radius(
            point, self.area_center_point, self.area_radius,
            units='km', label=self.map_area)
