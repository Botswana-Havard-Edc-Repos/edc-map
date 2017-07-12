import os

from django.conf import settings
from django.test import TestCase

from .mappers import TestMapper
from .models import TestModel


class TestMaperMixin(TestCase):

    def setUp(self):
        self.mapper = TestMapper()
        self.item = TestModel.objects.create(
            gps_target_lat=-24.656620, gps_target_lon=25.923488, area_name=self.mapper.map_area, distance_from_target=25.12)
        self.coordinates = self.mapper.get_coordinates(self.item)

    def test_grep_image(self):
        """Check if images are downloaded for 3 zoom levels."""

        zoom_level = 16
        while zoom_level < 19:
            path = os.path.join(settings.MEDIA_ROOT, str(
                self.item.pk) + str(zoom_level) + '.jpg')
            self.assertTrue(os.path.isfile(path))
            zoom_level += 1
