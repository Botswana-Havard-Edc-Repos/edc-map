from .base_mapper import BaseAreaMapper
from ..classes import site_mappers
from ..models import TestModel


class TestItemMapper(BaseAreaMapper):

    item_model = TestModel
    map_area = 'test_area'
    map_code = '91'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -24.656620
    gps_center_lon = 25.923488
    identifier_field_attr = 'location_identifier'
    radius = 5.5
    location_boundary = ()

site_mappers.register(TestItemMapper)
