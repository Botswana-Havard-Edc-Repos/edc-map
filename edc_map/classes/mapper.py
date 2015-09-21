import math

from datetime import date, timedelta
from geopy import Point
from geopy import distance

from django.conf import settings

from ..exceptions import MapperError


class Mapper(object):

    #  Remove setters and gets and use class variables
    map_code = None
    map_area = None

    item_model = None
    item_model_cls = None
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

    target_gps_lat_field_attr = None
    target_gps_lon_field_attr = None
    icons = None
    other_icons = None

    identifier_field_attr = None
    identifier_field_label = None
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

    landmarks = None

    intervention = None

    gps_center_lat = None
    gps_center_lon = None
    radius = None
    location_boundary = None

    def __init__(self, *args, **kwargs):
        self._item_model_cls = None
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
        self._target_gps_lon_field_attr = None
        self._target_gps_lat_field_attr = None
        self._map_area_field_attr = None
        self._map_code = None

    def __repr__(self):
        return 'Mapper({0.map_code!r}:{0.map_area!r})'.format(self)

    def __str__(self):
        return '({0.map_code!r}:{0.map_area!r})'.format(self)

    def _get_attr(self, attrname):
        if not attrname:  # attrname is the class variable name
            raise TypeError('attrname may not be None.')
        _name = '_{0}'.format(attrname)  # the instance variable name
        if not getattr(self, _name):  # if instance variable is not set
            getattr(self, 'set_{0}'.format(attrname))()
        return getattr(self, _name)

    def _set_attr(self, attrname, attr=None, allow_none=False):
        if attrname.startswith('_'):
            raise TypeError('attrname cannot start with \'_\'')
        if attr:
            setattr(self, '_{0}'.format(attrname), attr)  # set the instance variable to attr
        else:
            try:
                setattr(self, '_{0}'.format(attrname), getattr(self, attrname))  # set the instance variable to the value of the class variable.
            except:
                pass
        if not allow_none:
            if not getattr(self, '_{0}'.format(attrname)):
                raise MapperError('Attribute \'{0}\' may not be None.'.format(attrname))

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

    def prepare_map_points(self, items, selected_icon, cart, cart_icon,
                           dipatched_icon='red-circle.png',
                           selected_section="All",
                           selected_sub_section='ALL'):
        """Returns a list of item identifiers from the given queryset
        excluding those items that have been dispatched.
        """
        payload = []
        icon_number = 0
        if selected_section == "All":
            section_color_code_dict = self.make_dictionary(self.regions, self.icons)
        else:
            section_color_code_dict = self.make_dictionary(self.sections, self.other_icons)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                   "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        for item in items:
            identifier_label = str(getattr(item, self.identifier_field_attr))
            other_identifier_label = ""
#             # does nothing
#             if getattr(item, self.get_other_identifier_field_attr()):  # e.g. cso_number
#                 other_identifier_field_label = str("  {0}: ".format(self.other_identifier_field_label) +
#                                                    getattr(item, self.get_other_identifier_field_attr()))
            if item.is_dispatched_as_item():
                icon = dipatched_icon
                identifier_label = "{0} already dispatched".format(identifier_label)
            elif getattr(item, self.identifier_field_attr) in cart:  # e.g household_identifier
                icon = cart_icon
                identifier_label = "{0} in shopping cart waiting to be dispatched".format(identifier_label)
            else:
                icon = "blu-circle.png"
                if selected_section == "All":
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if getattr(item, self.region_field_attr) == key_sec:
                            icon = icon_value
                else:
                    for key_sec, icon_value in section_color_code_dict.iteritems():
                        if getattr(item, self.section_field_attr) == key_sec:
                            if icon_number <= 25:
                                icon = icon_value + letters[icon_number] + '.png'
                                icon_number += 1
                            if icon_number == 25:
                                icon_number = 0
            payload.append([getattr(item, self.target_gps_lon_field_attr),
                            getattr(item, self.target_gps_lat_field_attr),
                            identifier_label, icon, other_identifier_label])
        return payload

    def gps_distance_between_points(self, lat, lon, center_lat=None, center_lon=None):
        """Check if a GPS point is within the boundaries of a community

        This method uses geopy.distance and geopy.Point libraries to
        calculate the distance between two points and return the
        distance in units requested.

        The community_radius, community_center_lat and
        community_center_lon are from the Mapper class of each community.
        """
        center_lat = center_lat or self.gps_center_lat
        center_lon = center_lon or self.gps_center_lon
        pt1 = Point(float(lat), float(lon))
        pt2 = Point(float(center_lat), float(center_lon))
        dist = distance.distance(pt1, pt2).km
        return dist

    def deg_to_dms(self, deg):
        """Convert a latitude or longitude into degree minute GPS format
        """
        d = int(deg)
        md = (deg - d) * 60
        m = round(md, 3)
        if d < 0 and m < 0:
            d = -d
            m = -m
        return [d, m]

    def get_cardinal_point_direction(self, start_lat, start_lon, end_lat, end_lon):
        """Calculates the angle/Bearing of direction between two points
        on the earth and returns the distance between two points and
        the cardinal points direction.

        This method is for the initial bearing which if followed in
        a straight line along a great-circle arc will take you from
        the start point to the end point.
        """
        dist = self.distance_between_points(start_lat, start_lon, end_lat, end_lon)
        dlon = math.radians(end_lon - start_lon)
        start_lat = math.radians(start_lat)
        end_lat = math.radians(end_lat)
        y = math.sin(dlon) * math.cos(end_lat)
        x = math.cos(start_lat) * math.sin(end_lat) - math.sin(start_lat) * math.cos(end_lat) * math.cos(dlon)
        brng = math.degrees(math.atan2(y, x))
        bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        index = brng - 22.5
        if (index < 0):
            index += 360
        index = int(index / 45)

        return(round(dist, 3), bearings[index])

    def _get_gps(self, direction, degrees, minutes):
        """Converts GPS degree/minutes to latitude or longitude."""
        dct = {'s': -1, 'e': 1}
        if direction not in dct.keys():
            raise TypeError('Direction must be one of {0}. Got {1}.'.format(dct.keys(), direction))
        d = float(degrees)
        m = float(minutes)
        return dct[direction] * round((d) + (m / 60), 5)

    def get_gps_lat(self, d, m):
        """Converts degree/minutes S to latitude."""
        return self._get_gps('s', d, m)

    def get_gps_lon(self, d, m):
        """Converts degree/minutes E to longitude."""
        return self._get_gps('e', d, m)

    def verify_gps_location(self, lat, lon, exception_cls):
        """Verifies that given lat, lon occur within the community
        area and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        verify_gps_location = True
        try:
            verify_gps_location = settings.VERIFY_GPS_LOCATION
        except AttributeError:
            pass
        if verify_gps_location:
            dist = self.gps_distance_between_points(lat, lon)
            if dist > self.radius:
                raise exception_cls('The location (GPS {0} {1}) does not fall within area of \'{2}\'.'
                                    'Got {3}m'.format(lat, lon, self.map_area, dist * 1000))
        return True

    def verify_gps_to_target(self, lat, lon, center_lat, center_lon, radius, exception_cls, radius_bypass_instance=None):
        """Verifies the gps lat, lon occur within a radius of the
        target lat/lon and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        radius = radius or self.radius
        verify_gps_to_target = True  # default
        try:
            verify_gps_to_target = settings.VERIFY_GPS
        except AttributeError:
            pass
        if verify_gps_to_target:
            if not radius_bypass_instance:
                dist = self.gps_distance_between_points(lat, lon, center_lat, center_lon)
                if dist > radius:
                    raise exception_cls('GPS {0} {1} is more than {2} meters from the target location {3}/{4}. '
                                        'Got {5}m.'.format(lat, lon, radius * 1000, center_lat,
                                                           center_lon, dist * 1000))
            else:
                dist = self.gps_distance_between_points(
                    lat,
                    lon,
                    center_lat,
                    center_lon)
                if dist > radius_bypass_instance.bypass_radius:
                    raise exception_cls('GPS {0} {1} is more than {2} meters from the bypass target location {3}/{4}. '
                                        'Got {5}m.'.format(lat, lon, radius_bypass_instance.bypass_radius,
                                                           center_lat,
                                                           center_lon, dist * 1000))
        return True
