from django.test import TestCase

from edc_map.classes import site_mappers
from ..models import MapperMixin


class TestModel(MapperMixin):

    class Meta:
        app_label = 'edc_map'


class TestMapper(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        self.mapper = site_mappers.registry.get('test_area')
        self.item = TestModel.objects.create(
            gps_target_lat=24.124,
            gps_target_lon=22.343,
            area_name=self.mapper.map_area,
            distance_from_target=25.12)
        self.lat = None
        self.lon = None

        self.items = [self.item]

    def test_distance_between_points(self):
        self.assertRaises(TypeError, self.mapper.distance_between_points, self.lat, self.lon)
        self.assertEqual(
            self.mapper.distance_between_points(
                -24.656637, 25.924327, -24.656366, 25.922935), 0.14407256837110122, 'Correct distance if matching')

    def test_degrees_to_degrees_minutes_sec(self):
        self.assertEqual(
            self.mapper.deg_to_dms(-24.656637), [24, 39.398])
