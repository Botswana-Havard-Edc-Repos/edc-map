from edc_map.site_mappers import site_mappers

from edc_map.mapper import Mapper

from .landmarks import TEST_LANDMARKS


class AnonymousMapper(Mapper):

    map_area = 'austin'
    map_code = '88'
    center_lat = -30.2671500
    center_lon = 97.7430600
    radius = 100.5
    location_boundary = ()

    intervention = True
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS
    identifier_field_attr = 'plot_identifier'
    landmarks = None

site_mappers.register(AnonymousMapper)


class TestPlotMapper(Mapper):

    map_area = 'test_community'
    map_code = '01'
    pair = 0
    regions = None  # SECTIONS
    sections = None  # SUB_SECTIONS
    identifier_field_attr = 'plot_identifier'

    @property
    def sections(self):
        """Return a list of sections."""
        return ['A', 'B', 'C', 'D', 'E']

    @property
    def sub_sections(self):
        """Return a list of sub sections."""
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    landmarks = TEST_LANDMARKS

    center_lat = -25.330451
    center_lon = 25.556502
    radius = 100.5
    location_boundary = ()

    intervention = True

site_mappers.register(TestPlotMapper)
