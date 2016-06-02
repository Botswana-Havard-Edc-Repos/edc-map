from datetime import date, timedelta
# from geopy import Point, distance

from .choices import ICONS
from .geo_mixin import GeoMixin
from edc_map.exceptions import MapperError

LETTERS = list(map(chr, range(65, 91)))

LANDMARK_NAME = 0
LONGITUDE = 1
LATITUDE = 2


class Mapper(GeoMixin):

    map_code = None
    map_area = None
    radius = 5.5
    identifier_field_attr = None

    identifier_field_label = None

    item_model = None
    item_label = None

    region_field_attr = None
    region_label = None
    section_field_attr = None
    section_label = None
    map_area_field_attr = None

    # different map fields, the numbers are the zoom levels
    map_field_attr_18 = None
    map_field_attr_17 = None
    map_field_attr_16 = None

    icons = ICONS
    other_icons = None

    other_identifier_field_attr = None
    other_identifier_field_label = None

    item_target_field = None
    item_selected_field = None

    gps_degrees_s_field_attr = None
    gps_degrees_e_field_attr = None
    gps_minutes_s_field_attr = None
    gps_minutes_e_field_attr = None

    regions = None
    sections = None

    landmarks = None  # format ((name, longitude, latitude), )

    intervention = None

    def __init__(self, *args, **kwargs):
        self._item_label = None
        self._regions = None
        self._map_field_attr_18 = None
        self._map_field_attr_17 = None
        self._map_field_attr_16 = None
        self._item_selected_field = None
        self._sections = None
        self._icons = None
        self._other_icons = None
        self._landmarks = None
        self._region_label = None
        self._section_label = None
        self._region_field_attr = None
        self._section_field_attr = None
        self._identifier_field_attr = None
        self._identifier_label = None
        self._other_identifier_field_attr = None  # e.g. cso_number
        self._other_identifier_label = None
        self._gps_center_lon = None
        self._map_area_field_attr = None
        self._map_code = None

    def __repr__(self):
        return 'Mapper({0.map_code!r}:{0.map_area!r})'.format(self)

    def __str__(self):
        return '({0.map_code!r}:{0.map_area!r})'.format(self)

    def prepare_created_filter(self):
        """Need comment"""
        date_list_filter = []
        today = date.today() + timedelta(days=0)
        tomorrow = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=1)
        last_7days = date.today() - timedelta(days=7)
        last_30days = date.today() - timedelta(days=30)
        # created__lt={0},created__gte={1}
        date_list_filter.append(["Any date", ""])
        date_list_filter.append(["Today", "{0},{1}".format(tomorrow, today)])
        date_list_filter.append(["Yesterday", "{0},{1}".format(today, yesterday)])
        date_list_filter.append(["Past 7 days", "{0},{1}".format(tomorrow, last_7days)])
        date_list_filter.append(["Past 30 days", "{0},{1}".format(tomorrow, last_30days)])
        return date_list_filter

    def make_dictionary(self, list1, list2):
        """Need comment"""
        # the shortest list should be the first list if the lists do
        # not have equal number of elements
        sec_icon_dict = {}
        for sec, icon in zip(list1, list2):
            if sec:
                sec_icon_dict[sec] = icon
            else:
                break
        return sec_icon_dict

    def session_to_string(self, identifiers, new_line=True):
        val = ""
        delim = ", "
        if identifiers:
            for identifier in identifiers:
                val = val + identifier + delim
        return val

    def get_coordinates(self, item):
        """Return target coordinates of a location."""
        latitude = str(item.gps_target_lat)
        longitude = str(item.gps_target_lon)
        return [latitude, longitude]

    @property
    def area_center_point(self):
        return (self.gps_center_lat, self.gps_center_lon)

    @property
    def area_radius(self):
        return self.radius

    def point_in_map_area(self, point):
        """Return True if point is within mapper area radius."""
        return self.point_in_radius(
            point, self.area_center_point, self.area_radius)

    def raise_if_not_in_map_area(self, point):
        self.raise_if_not_in_radius(
            point, self.area_center_point, self.area_radius,
            units='km', label=self.map_area)
