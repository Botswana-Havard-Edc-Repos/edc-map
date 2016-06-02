import factory

from django.test import TestCase

from ..contants import CONFIRMED, UNCONFIRMED
# from ..classes import site_mappers
from ..exceptions import MapperError
from ..models import MapperMixin
from edc_map.mappers import TestItemMapper


class TestModel(MapperMixin):

    class Meta:
        app_label = 'edc_map'


class TestModelFactory(factory.DjangoModelFactory):

    class Meta:
        model = TestModel

    gps_target_lon = factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '2.12345{0}'.format(n))


class TestLocationConfirmation(TestCase):

    def setUp(self):
        self.mapper = TestItemMapper()
        self.item = TestModel.objects.create(gps_target_lat=-24.656620, gps_target_lon=25.923488, area_name=self.mapper.map_area, distance_from_target=25.12)

    def test_unconfirm_item(self):
        """Test if a plot has no confirmation coordinates, its action is unconfirmed."""

        self.assertEqual(self.item.action, UNCONFIRMED)

    def test_confirm_item(self):
        """Test if an item with confirmation coordinates, its action becomes confirmed."""

        self.item.gps_confirm_latitude = -24.656620
        self.item.gps_confirm_longitude = 25.923488
        self.item.save()
        self.assertEqual(self.item.action, CONFIRMED)

    def test_point_in_map_area(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirm_latitude': -24.664542,
            'gps_confirm_longitude': 25.783037,
            'area_name': self.mapper.map_area,
            'gps_target_lat': -24.656620,
            'gps_target_lon': 25.923488}
        with self.assertRaises(MapperError) as context:
            TestModelFactory(**data)
        self.assertIn(
            'The location (GPS -24.664542 25.783037) does not fall within area of \'test_area\'.Got 14244.29755501753m',
            str(context.exception))

    def test_point_in_radius(self):
        """Test if an item is outside a map area raises a mapper error."""

        data = {
            'gps_confirm_latitude': -24.656630,
            'gps_confirm_longitude': 25.921718,
            'area_name': self.mapper.map_area,
            'gps_target_lat': -24.656620,
            'gps_target_lon': 25.923488}
        with self.assertRaises(MapperError) as context:
            TestModelFactory(**data)
        self.assertIn(
            'GPS -24.65663 25.921718 is more than 25.0 meters from the target location -24.65662/25.923488. Got 179.17846793158006m.',
            str(context.exception))
