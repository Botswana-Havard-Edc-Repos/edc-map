import os

from django.conf import settings
from django.test import TestCase

from ..snapshot import Snapshot
from .mappers import TestItemMapper
from .models import TestModel


class TestSnapshot(TestCase):

    def setUp(self):
        self.mapper = TestItemMapper()
        self.test_model = TestModel.objects.create(
            gps_target_lat=24.124,
            gps_target_lon=22.343,
            map_area=self.mapper.map_area,
            distance_from_target=25.12)
        self.coordinates = self.mapper.get_coordinates(self.test_model)
        self.snapshot = Snapshot()

    def test_coordinates(self):
        """Check if coordinates are returned for an existing item.
        """

        self.assertEqual(self.coordinates, ['24.124', '22.343'])

    def test(self):
        """Test if an item url is returned, without landmarks and a zoom level."""

        url = self.snapshot.google_image_url(self.coordinates)
        expected_url = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32&zoom=None&center=24.124,22.343&markers=color:red%7C24.124,22.343&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&sensor=false'
        self.assertEqual(url, expected_url)

    def test_grep_image(self):
        """Check if an image if downloaded."""

        path = os.path.join(settings.MEDIA_ROOT, 'img.jpg')
        url = self.snapshot.google_image_url(self.coordinates)
        self.snapshot.grep_image(url, 'img')
        self.assertTrue(os.path.isfile(path))

    def test_image_file_url(self):
        """Test if a local stored image url is generated."""

        obj_pk = 'wer23rf23r2rf5h56h5nbs5'
        path = os.path.join(settings.MEDIA_URL, obj_pk + '.jpg')
        url = self.snapshot.google_image_url(self.coordinates)
        self.snapshot.grep_image(url, obj_pk)
        url = self.snapshot.image_file_url(obj_pk)
        self.assertEqual(url, path)
