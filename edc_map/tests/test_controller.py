from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from edc_map.classes import Controller, site_mappers
from edc_map.exceptions import MapperError, AlreadyRegistered
from edc_map.classes.mapper import Mapper

from .mappers import TestPlotMapper1, TestPlotMapper2, TestPlotMapper3


class TestPlotMapperDup(Mapper):
    map_area = 'test_community_dup'
    map_code = '99'
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


class TestController(TestCase):

    def setUp(self):
        self.current_community = 'test_community1'
        TestPlotMapperDup.map_area = 'test_community_dup'
        TestPlotMapperDup.map_code = '99'

    @override_settings(CURRENT_COMMUNITY='test_community2')
    def test_controller_loads_current_mapper_from_settings(self):
        test_site_mappers = Controller()
        test_site_mappers.register(TestPlotMapper3)
        test_site_mappers.register(TestPlotMapper2)
        test_site_mappers.register(TestPlotMapper1)
        self.assertEqual(test_site_mappers.current_mapper.map_code, TestPlotMapper2.map_code)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_controller_loads_current_mapper_on_register(self):
        test_site_mappers = Controller(current_community=self.current_community)
        test_site_mappers.register(TestPlotMapper1)
        self.assertEqual(test_site_mappers.current_mapper.map_area, settings.CURRENT_COMMUNITY)

    def test_controller_raises_on_wrong_current_mapper(self):
        test_site_mappers = Controller(current_community=self.current_community)
        test_site_mappers.register(TestPlotMapper2)
        self.assertRaises(MapperError, test_site_mappers.load_current_mapper, TestPlotMapper2)
        mappers = Controller(current_community='test_community2')
        mappers.load_current_mapper(TestPlotMapper2)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_controller_detects_duplication(self):
        test_site_mappers = Controller()
        test_site_mappers.register(TestPlotMapper3)
        test_site_mappers.register(TestPlotMapper2)
        test_site_mappers.register(TestPlotMapper1)
        self.assertRaises(AlreadyRegistered, test_site_mappers.register, TestPlotMapperDup)
        TestPlotMapperDup.map_area = 'test_community1'
        TestPlotMapperDup.map_code = '10'
        self.assertRaises(AlreadyRegistered, test_site_mappers.register, TestPlotMapperDup)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_controller_detects_nones(self):
        test_site_mappers = Controller()
        TestPlotMapperDup.map_area = None
        TestPlotMapperDup.map_code = '10'
        self.assertRaises(MapperError, test_site_mappers.register, TestPlotMapperDup)
        TestPlotMapperDup.map_area = 'test_community1'
        TestPlotMapperDup.map_code = None
        self.assertRaises(MapperError, test_site_mappers.register, TestPlotMapperDup)
        TestPlotMapperDup.map_area = None
        TestPlotMapperDup.map_code = None
        self.assertRaises(MapperError, test_site_mappers.register, TestPlotMapperDup)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_controller_autodiscover(self):
        site_mappers.autodiscover('tests.registered_mappers')
        self.assertIn(TestPlotMapper1().map_area, site_mappers.map_areas)
        self.assertIn(TestPlotMapper1().map_code, site_mappers.map_codes)
