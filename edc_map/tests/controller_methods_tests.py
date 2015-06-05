from django.test import TestCase
from django.conf import settings

from ..classes import site_mappers
from ..exceptions import MapperError


class ControllerTests(TestCase):

    def test_controller_methods(self):

        site_mappers.autodiscover()
        # Test the  get_current_mapper method
        self.assertRaises(MapperError, site_mappers.get_current_mapper().map_area)
        self.assertTrue('CURRENT_COMMUNITY' in dir(settings), 'Settings attribute CURRENT_COMMUNITY not found')
        self.assertTrue(settings.CURRENT_COMMUNITY, 'Settings attribute CURRENT_COMMUNITY needs to have a value')