import os

from django.test import TestCase

from ..models import MapperMixin
from edc_map.mappers import TestItemMapper
from django.conf import settings


class TestModel(MapperMixin):

    class Meta:
        app_label = 'edc_map'


class TestMaperMixin(TestCase):

    def setUp(self):
        self.mapper = TestItemMapper()
        self.item = TestModel.objects.create(gps_target_lat=24.124, gps_target_lon=22.343, area_name=self.mapper.map_area, distance_from_target=25.12)
        self.coordinates = self.mapper.get_coordinates(self.item)

    def test_grep_image(self):
        """Check if images are downloaded for 3 zoom levels."""

        zoom_level = 16
        while zoom_level < 19:
            path = os.path.join(settings.MEDIA_ROOT, str(self.item.pk) + str(zoom_level) + '.jpg')
            self.assertTrue(os.path.isfile(path))
            zoom_level += 1
