import os

from django.conf import settings
from django.test import TestCase

from ..site_mappers import site_mappers
from ..snapshot import Snapshot
from .models import TestModel


class TestSnapshot(TestCase):

    def setUp(self):
        self.center_lat = -25.011111
        self.center_lon = 25.741111
        self.test_model = TestModel.objects.create(
            gps_target_lat=self.center_lat,
            gps_target_lon=self.center_lon,
            map_area=site_mappers.current_map_area)
        self.coordinates = [self.center_lat, self.center_lon]
        self.snapshot = Snapshot(
            'img', self.test_model.target_point, site_mappers.current_map_area)

    def test(self):
        """Test if an item url is returned, without landmarks and a zoom level."""

        url = self.snapshot.image_url(17)
        expected_url = 'http://maps.google.com/maps/api/staticmap?center=-25.011111%2C25.741111&format=png32&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&maptype=satellite&scale=2&sensor=false&size=640x600&zoom=17&markers=color%3Ared%7C-25.011111%2C25.741111'
        self.assertEqual(url, expected_url)

    def test_grep_image(self):
        """Check if an image if downloaded."""

        path = os.path.join(settings.MEDIA_ROOT, 'edc_map', 'img17.jpg')
        self.snapshot.image_url(17)
        self.snapshot.retrieve_and_store_image(17)
        self.assertTrue(os.path.isfile(path))
