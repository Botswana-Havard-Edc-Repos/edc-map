from django.test import TestCase

from ..contants import CONFIRMED, UNCONFIRMED
# from ..classes import site_mappers
from ..exceptions import MapperError
from ..models import MapperMixin
from .factories import MapperMixinFactory
from edc_map.mappers import TestItemMapper


class TestLocationConfirmation(TestCase):

    def setUp(self):
        self.mapper = TestItemMapper()
        self.item = MapperMixin.objects.create(gps_target_lat=24.124, gps_target_lon=22.343, area_name=self.mapper.map_area, distance_from_target=25.12)

    def test_unconfirm_item(self):
        """Test if a plot has no confirmation coordinates, its action is unconfirmed."""

        self.assertEqual(self.item.action, UNCONFIRMED)

    def test_confirm_item(self):
        """Test if an item with confirmation coordinates, its action becomes confirmed."""

        self.item.gps_confirm_latitude = 24.124
        self.item.gps_confirm_longitude = 22.343
        self.item.save()
        self.assertEqual(self.item.action, CONFIRMED)

    def test_location_in_map_area(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirm_latitude': -24.666,
            'gps_confirm_longitude': 23.343,
            'area_name': self.mapper.map_area,
            'gps_target_lat': 24.124,
            'gps_target_lon': 22.343}
        with self.assertRaises(MapperError) as context:
            MapperMixinFactory(**data)
        self.assertIn('The location (GPS -24.666 23.343) does not fall within area of \'test_area\'.Got 5399157.515971059m', str(context.exception))

    def test_location_in_target(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirm_latitude': -24.666,
            'gps_confirm_longitude': 23.343,
            'area_name': self.mapper.map_area,
            'gps_target_lat': 24.124,
            'gps_target_lon': 22.343}
        with self.assertRaises(MapperError) as context:
            MapperMixinFactory(**data)
        self.assertIn('The location (GPS -24.666 23.343) does not fall within area of \'test_area\'.Got 5399157.515971059m', str(context.exception))
