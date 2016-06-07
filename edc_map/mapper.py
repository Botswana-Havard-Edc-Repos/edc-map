from geopy import Point

from .geo_mixin import GeoMixin
from django.apps import apps as django_apps

LETTERS = list(map(chr, range(65, 91)))

LANDMARK_NAME = 0
LONGITUDE = 1
LATITUDE = 2


class Mapper(GeoMixin):

    app_config = django_apps.get_app_config('edc_map')
    center_lat = None
    center_lon = None
    landmarks = None  # format ((name, longitude, latitude), )
    map_area = None
    radius = 5.5

    def __init__(self):
        self.name = self.map_area or 'mapper {}'.format(self.__class__.name)
        try:
            self.item_model = django_apps.get_model(*self.app_config.mapper_model)
            self.item_model_cls = self.item_model
            self.item_label = self.item_model._meta.verbose_name
        except LookupError as e:
            print('  Warning. Lookup error in mapper {}. Got {}'.format(self.name, str(e)))
        try:
            self.survey_model = django_apps.get_model(*self.app_config.mapper_survey_model)
        except LookupError as e:
            print('  Warning. Lookup error in mapper {}. Got {}'.format(self.name, str(e)))
        self.load()

    def __repr__(self):
        return 'Mapper({0.map_area!r})'.format(self)

    def __str__(self):
        return '({0.map_area!r})'.format(self)

    def load(self):
        LandmarkModel = django_apps.get_model(*self.app_config.landmark_model)
        MapperDataModel = django_apps.get_model(*self.app_config.mapper_data_model)
        return None

    @property
    def __dict__(self):
        return {
            'map_area': self.map_area,
            'gps_center_lat': self.gps_center_lat,
            'gps_center_lon': self.gps_center_lon,
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
