from django.test import TestCase
from django.db import models

from ..contants import CONFIRMED, UNCONFIRMED
# from ..classes import site_mappers
from ..exceptions import MapperError
from ..models import MapperMixin
from .factories import MapperMixinFactory
from ..area_map import TestItemMapper


class TestModel(models.Model):

    gps_lon = models.DecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_lat = models.DecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    target_radius = models.FloatField(
        default=.025,
        help_text='km',
        editable=False)

    distance_from_target = models.FloatField(
        null=True,
        editable=True,
        help_text='distance in meters')

    area_name = models.CharField(
        max_length=25,
        help_text='If the area name is incorrect, please contact the DMC immediately.',
        editable=False)

    class Meta:
        app_label = 'edc_map'


class TestSnapshot(TestCase):

    def setUp(self):
#         self.mapper = site_mappers.get_mapper('test_area')
        self.mapper = TestItemMapper()
        self.item = MapperMixin.objects.create(gps_target_lat=24.124, gps_target_lon=22.343, area_name=self.mapper.map_area, distance_from_target=25.12)
        self.coordinates = self.mapper.get_coordinates(self.mapper.items(self.mapper.map_area)[0])

    def test_coordinates(self):
        """Check if coordinates are returned for an existing item."""

        self.assertEqual(self.coordinates, ['24.124', '22.343'])

    def test(self):
        """Test if an item url is returned, without landmarks and a zoom level."""

        url = self.mapper.image_url(self.coordinates)
        expected_url = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32&zoom=None&center=24.124,22.343&markers=color:red%7C24.124,22.343&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&sensor=false'
        self.assertEqual(url, expected_url)

    def test_grep_image(self):
        """Check if an image if downloaded."""

        path = '/Users/ckgathi/Desktop/'
        url = self.mapper.image_url(self.coordinates)
        self.mapper.grep_image(url, path, 'imgd')

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
        """Test if an item is outside a map area."""

        data = {
            'gps_confirm_latitude': -24.666,
            'gps_confirm_longitude': 23.343,
            'area_name': self.mapper.map_area,
            'gps_target_lat': 24.124,
            'gps_target_lon': 22.343}
        with self.assertRaises(MapperError):
            MapperMixinFactory(**data)
