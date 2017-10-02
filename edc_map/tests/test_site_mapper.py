from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from ..exceptions import AlreadyRegistered
from ..mapper import Mapper
from ..site_mappers import SiteMapperError
from ..site_mappers import SiteMappers, site_mappers


class TestMapperDup(Mapper):
    map_area = 'test_community1'
    map_code = '99'
    regions = []
    sections = []
    landmarks = []
    center_lat = -25.011111
    center_lon = 25.741111
    radius = 5.5
    location_boundary = ()
    mapper_model = 'edc_map.testmodel'


class TestMapper1(Mapper):
    map_area = 'test_community1'
    map_code = '99'
    regions = []
    sections = []
    landmarks = []
    center_lat = -25.011111
    center_lon = 25.741111
    radius = 5.5
    location_boundary = ()
    mapper_model = 'edc_map.testmodel'


site_mappers.register(TestMapper1)


class TestMapper2(Mapper):
    map_area = 'test_community2'
    map_code = '98'
    regions = []
    sections = []
    landmarks = []
    center_lat = -25.011111
    center_lon = 25.741111
    radius = 5.5
    location_boundary = ()
    mapper_model = 'edc_map.testmodel'


site_mappers.register(TestMapper2)


class TestMapper3(Mapper):
    map_area = 'test_community3'
    map_code = '97'
    regions = []
    sections = []
    landmarks = []
    center_lat = -25.011111
    center_lon = 25.741111
    radius = 5.5
    location_boundary = ()
    mapper_model = 'edc_map.testmodel'


site_mappers.register(TestMapper3)


class TestSiteMappers(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        self.current_community = 'test_community1'
        TestMapperDup.map_area = 'test_community_dup'
        TestMapperDup.map_code = '99'

    @override_settings(CURRENT_COMMUNITY='test_community2')
    def test_site_mappers_loads_current_mapper_from_settings(self):
        test_site_mappers = SiteMappers()
        test_site_mappers.register(TestMapper3)
        test_site_mappers.register(TestMapper2)
        test_site_mappers.register(TestMapper1)
        self.assertEqual(
            test_site_mappers.current_mapper.map_code, TestMapper1.map_code)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_site_mappers_loads_current_mapper_on_register(self):
        test_site_mappers = SiteMappers(
            current_map_area=self.current_community)
        test_site_mappers.register(TestMapper1)
        self.assertEqual(test_site_mappers.current_mapper.map_area,
                         settings.CURRENT_COMMUNITY)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_site_mappers_detects_duplication(self):
        test_site_mappers = SiteMappers()
        test_site_mappers.register(TestMapper3)
        test_site_mappers.register(TestMapper2)
        test_site_mappers.register(TestMapper1)
        self.assertRaises(AlreadyRegistered,
                          test_site_mappers.register, TestMapperDup)
        TestMapperDup.map_area = 'test_community1'
        TestMapperDup.map_code = '10'
        self.assertRaises(AlreadyRegistered,
                          test_site_mappers.register, TestMapperDup)

    @override_settings(CURRENT_COMMUNITY='test_community1')
    def test_site_mappers_detects_nones(self):
        test_site_mappers = SiteMappers()
        TestMapperDup.map_area = None
        TestMapperDup.map_code = '10'
        self.assertRaises(
            SiteMapperError, test_site_mappers.register, TestMapperDup)
        TestMapperDup.map_area = 'test_community1'
        TestMapperDup.map_code = None
        self.assertRaises(
            SiteMapperError, test_site_mappers.register, TestMapperDup)
        TestMapperDup.map_area = None
        TestMapperDup.map_code = None
        self.assertRaises(
            SiteMapperError, test_site_mappers.register, TestMapperDup)

    @override_settings(CURRENT_COMMUNITY='test_area')
    def test_site_mappers_autodiscover(self):
        site_mappers.autodiscover('tests.registered_mappers')
        self.assertIn(TestMapper1().map_area, site_mappers.map_areas)
        self.assertIn(TestMapper1().map_code, site_mappers.map_codes)
