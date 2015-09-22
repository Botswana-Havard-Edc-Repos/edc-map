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
    target_gps_lon_field_attr = 'gps_target_lon'
    target_gps_lat_field_attr = 'gps_target_lat'
    identifier_field_attr = 'plot_identifier'

site_mappers.register(TestPlotMapper)


class TestMapper(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        self.mapper = site_mappers.registry.get('test_community')
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
        self.assertRaises(TypeError, self.mapper.gps_distance_between_points, self.lat, self.lon)
        self.assertEqual(
            self.mapper.gps_distance_between_points(
                -24.656637, 25.924327, -24.656366, 25.922935), 0.14407256837110122, 'Correct distance if matching')

    def test_degrees_to_degrees_minutes_sec(self):
        self.assertEqual(
            self.mapper.deg_to_dms(-24.656637), [24, 39.398])

    def test_verify_gps_to_target(self):
        self.assertEqual(self.mapper.location_in_target(
            -24.656637, 25.924327, -24.656637, 25.924327, 0.025, MapperError),
            True,
            'The is the same point targeted')
        self.assertEqual(self.mapper.prepare_map_points(
            self.items, selected_icon='', cart='', cart_icon='egg-circle.png',
            dipatched_icon='red-circle.png', selected_section="All", selected_sub_section='ALL'),
            [[25.745569, -25.032927, getattr(self.items[0], self.mapper.identifier_field_attr), 'blu-circle.png', '']])
