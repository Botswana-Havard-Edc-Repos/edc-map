from django.test import TestCase

from edc_map.classes import site_mappers
from edc_map.classes import Mapper
from edc_map.exceptions import MapperError

from .test_plot import Plot


class TestPlotMapper(Mapper):
    map_area = 'test_community'
    map_code = '999'
    identifier_field_attr = 'plot_identifier'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.011111
    gps_center_lon = 25.741111
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestPlotMapper)


class TestMapper(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        self.mapper = site_mappers.get_registry('test_community')()
        self.plot = Plot.objects.create(
            plot_identifier='12345',
            community='test_community',
            gps_target_lon=25.745569,
            gps_target_lat=-25.032927
        )
        self.lat = None
        self.lon = None

        self.items = [self.plot]

    def test_distance_between_points(self):
        self.assertRaises(MapperError, self.mapper.gps_distance_between_points, self.lat, self.lon)
        self.assertEqual(
            self.mapper.gps_distance_between_points(
                -24.656637, 25.924327, -24.656366, 25.922935), 0.14407256837110122, 'Correct distance if matching')

    def test_deggrees_to(self):
        self.assertEqual(self.mapper.deg_to_dm(-24.656637), [24.0, 39.39822000000004],
                         'converted to this: -24.656637 to this : 24.0, 39.39822000000004]')

    def test_cardinal_point_direction(self):
        self.assertEqual(self.mapper.get_cardinal_point_direction(
            -24.656637, 25.924327, -24.656366, 25.922935), (0.144, 'W'),
            'Direction and distance between two point')

    def test_verify_gps_to_target(self):
        self.assertEqual(self.mapper.verify_gps_to_target(
            -24.656637, 25.924327, -24.656637, 25.924327, 0.025, MapperError),
            True,
            'The is the same point targeted')
        self.assertEqual(self.mapper.prepare_map_points(
            self.items, selected_icon='', cart='', cart_icon='egg-circle.png',
            dipatched_icon='red-circle.png', selected_section="All", selected_sub_section='ALL'),
            [25.745569, -25.032927, getattr(self.items[0], self.mapper.identifier_field_attr),
             'blue-circle.png', ''])
