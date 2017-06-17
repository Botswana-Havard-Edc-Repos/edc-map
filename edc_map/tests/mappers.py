from ..mapper import Mapper


class TestItemMapper(Mapper):

    map_area = 'test_community'
    map_code = '01'
    mapper_model = 'edc_map.testmodel'
    pair = 0
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS
    identifier_field_attr = 'item_identifier'

    @property
    def sections(self):
        """Return a list of sections."""
        return ['A', 'B', 'C', 'D', 'E']

    @property
    def sub_sections(self):
        """Return a list of sub sections."""
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    landmarks = []

    center_lat = -25.330451
    center_lon = 25.556502
    radius = 100.5
    location_boundary = ()

    intervention = True
