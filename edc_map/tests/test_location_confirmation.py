from django.test import TestCase

from ..exceptions import MapperError
from .models import TestModel
from edc_map.site_mappers import site_mappers


class TestLocationConfirmation(TestCase):

    def setUp(self):
        self.center_lat = -25.011111
        self.center_lon = 25.741111
        self.item = TestModel.objects.create(
            gps_target_lat=self.center_lat, gps_target_lon=self.center_lon, map_area=site_mappers.current_map_area)

    def test_unconfirm_item(self):
        """Test if a plot has no confirmation coordinates, its action is unconfirmed."""

        self.assertFalse(self.item.confirmed)

    def test_confirm_item(self):
        """Test if an item with confirmation coordinates, its action becomes confirmed."""
        self.item.gps_confirmed_latitude = self.center_lat
        self.item.gps_confirmed_longitude = self.center_lon
        self.item.save()
        self.item = TestModel.objects.get(id=self.item.id)
        self.assertTrue(self.item.confirmed)

    def test_point_in_map_area(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirmed_latitude': -24.664542,
            'gps_confirmed_longitude': 25.783037,
            'map_area': site_mappers.current_map_area,
            'gps_target_lat': self.center_lat,
            'gps_target_lon': self.center_lon}
        with self.assertRaises(MapperError) as context:
            TestModel.objects.create(**data)
        self.assertIn(
            'Invalid confirmation GPS point. Got GPS (-24.664542, 25.783037) is more than 5.5km from test_community1 (-25.011111, 25.741111). Got 38.62km.',
            str(context.exception))

    def test_point_in_radius(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirmed_latitude': -24.65663,
            'gps_confirmed_longitude': 25.921718,
            'map_area': site_mappers.current_map_area,
            'gps_target_lat': self.center_lat,
            'gps_target_lon': self.center_lon}
        with self.assertRaises(MapperError) as context:
            TestModel.objects.create(**data)
        self.assertIn(
            'Invalid confirmation GPS point. Got GPS (-24.65663, 25.921718) is more than 5.5km from test_community1 (-25.011111, 25.741111). Got 43.3km.',
            str(context.exception))
