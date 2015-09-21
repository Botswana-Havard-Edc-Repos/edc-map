from django.test import TestCase

from edc_map.classes import site_mappers
from edc_map.exceptions import MapperError

from .test_plot import Plot


class ControllerTests(TestCase):

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

    def test_controller_methods(self):

        self.assertRaises(MapperError, site_mappers.get_current_mapper)
