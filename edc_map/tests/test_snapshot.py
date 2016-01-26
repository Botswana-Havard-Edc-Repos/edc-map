import os

from django.test import TestCase
from django.db import models

from ..models import MapperMixin
from ..area_map import TestItemMapper
from django.conf import settings


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
        self.mapper = TestItemMapper()
        self.item = MapperMixin.objects.create(gps_target_lat=24.124, gps_target_lon=22.343, area_name=self.mapper.map_area, distance_from_target=25.12)
        self.coordinates = self.mapper.get_coordinates(self.mapper.items(self.mapper.map_area)[0])

    def test_coordinates(self):
        """Check if coordinates are returned for an existing item."""

        self.assertEqual(self.coordinates, ['24.124', '22.343'])

    def test(self):
        """Test if an item url is returned, without landmarks and a zoom level."""

        url = self.mapper.google_image_url(self.coordinates)
        expected_url = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32&zoom=None&center=24.124,22.343&markers=color:red%7C24.124,22.343&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&sensor=false'
        self.assertEqual(url, expected_url)

    def test_grep_image(self):
        """Check if an image if downloaded."""

        path = os.path.join(settings.MEDIA_ROOT, 'img.jpg')
        url = self.mapper.google_image_url(self.coordinates)
        self.mapper.grep_image(url, 'img')
        self.assertTrue(os.path.isfile(path))

    def test_image_file_url(self):
        """Test if a local stored image url is generated."""

        obj_pk = 'wer23rf23r2rf5h56h5nbs5'
        path = os.path.join(settings.MEDIA_ROOT, obj_pk + '.jpg')
        url = self.mapper.google_image_url(self.coordinates)
        self.mapper.grep_image(url, obj_pk)
        url = self.mapper.image_file_url(obj_pk)
        self.assertEqual(url, path)
