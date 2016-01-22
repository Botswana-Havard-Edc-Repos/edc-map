from .base_mapper import BaseAreaMapper
# from ..classes import site_mappers


class TestItemMapper(BaseAreaMapper):

    item_model = 'MapperMixin'
    map_area = 'test_area'
    map_code = '99'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = 24.124
    gps_center_lon = 22.343
    radius = 5.5
    location_boundary = ()

# site_mappers.register(TestItemMapper)
