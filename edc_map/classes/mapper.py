import os

try:
    # Django versions >= 1.9
    from urllib.request import urlretrieve
except ImportError:
    # Django versions < 1.9
    from urllib import urlretrieve
from time import sleep

from datetime import date, timedelta
from geopy import Point
from geopy import distance
from operator import itemgetter

from django.conf import settings

from ..choices import ICONS
from ..exceptions import MapperError

LETTERS = list(map(chr, range(65, 91)))


class Mapper(object):

    map_code = None
    map_area = None
    radius = 5.5
    identifier_field_attr = 'plot_identifier'

    identifier_field_label = 'Plot Identifier'

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

    landmarks = None

    intervention = None

    gps_center_lat = None
    gps_center_lon = None

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
        for item in items:
            identifier_label = str(getattr(item, self.identifier_field_attr))
            other_identifier_label = ""

            # edc_dispatch method ??
            try:
                is_dispatched = item.is_dispatched_as_item()
            except AttributeError:
                is_dispatched = None

            if is_dispatched:
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
                                icon = icon_value + LETTERS[icon_number] + '.png'
                                icon_number += 1
                            if icon_number == 25:
                                icon_number = 0
            payload.append([getattr(item, self.target_gps_lon_field_attr),
                            getattr(item, self.target_gps_lat_field_attr),
                            identifier_label, icon, other_identifier_label])
        return payload

    def get_coordinates(self, item):
        """Return target coordinates of a location."""
        latitude = str(item.gps_target_lat)
        longitude = str(item.gps_target_lon)
        return [latitude, longitude]

    def zoom(self, zoom_level):
        """Return google map image zoom level url."""
        return '&zoom=' + str(zoom_level)

    def google_image_url(self, coordinates, landmarks=None, zoom_level=None):
        """Return the url of a google map image."""
        try:
            latitude, longitude = coordinates
        except ValueError:
            pass
        #  TODO fix pep8
        url = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32'
        url += self.zoom(zoom_level) + '&center=' + str(latitude) + ',' + str(longitude)
        url += self.landmarks_url(coordinates, landmarks) + '&markers=color:red%7C' + str(latitude) + ','
        url += str(longitude) + '&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&sensor=false'
        return url

    def close_landmarks(self, coordinates, landmarks):
        """Return landmarks sorted by close distance to the target location.

        Keyword arguments:
            coordinates: a list of coordinates pair, e.g [latitude, longitude].
            landmarks: a list of a list of landmarks, e.g [[landmark_name, latitude, longitude],].
        """
        latitude = 0.0
        longitude = 0.0
        try:
            latitude, longitude = coordinates
        except ValueError:
            pass
        distance_landmarks = []
        landmarks_dictionary = {}
        if landmarks:
            for landmark in landmarks:
                distance = self.gps_distance_between_points(latitude, longitude, landmark[1], landmark[2])
                distance_landmarks.append([distance, landmark[0], landmark[1], landmark[2]])
            landmarks = sorted(distance_landmarks, key=itemgetter(0))
            landmarks_dictionary = dict(zip(LETTERS, landmarks))
        return landmarks_dictionary

    def landmarks_url(self, coordinates, landmarks):
        """Return url for landmakrs to add to google map image url."""
        markers_str = ''
        close_landmarks = self.close_landmarks(coordinates, landmarks)
        for lable, landmark_values in close_landmarks.iteritems():
            if lable:
                markers_str += '&markers=color:blue%7Clabel:' + lable + '%7C' + str(landmark_values[2]) + ','
                markers_str += str(landmark_values[3])
        return markers_str

    def grep_image(self, url, image_name):
        """Grep a google map image and store in a location."""

        file_path = settings.MEDIA_ROOT
        image_path = os.path.join(file_path, image_name + '.jpg')
        if os.path.exists(file_path):
            urlretrieve(url, image_path)
            sleep(2)
        else:
            raise MapperError("The path {0} provided does not exist.".format(file_path))

    def location_in_map_area(self, lat, lon, exception_cls):
        """Verifies that given lat, lon occur within the community
        area and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        distance = self.gps_distance_between_points(lat, lon)
        if distance > self.radius:
            raise exception_cls('The location (GPS {0} {1}) does not fall within area of \'{2}\'.'
                                'Got {3}m'.format(lat, lon, self.map_area, distance * 1000))
        return True

    def location_in_target(self, lat, lon, center_lat, center_lon, radius, exception_cls, custom_radius=None):
        """Verifies the gps lat, lon occur within a radius of the
        target lat/lon and raises an exception if not.

        Wrapper for :func:`gps_validator`"""
        radius = radius or self.radius
        if not custom_radius:
            distance = self.gps_distance_between_points(lat, lon, center_lat, center_lon)
            if distance > radius:
                raise exception_cls('GPS {0} {1} is more than {2} meters from the target location {3}/{4}. '
                                    'Got {5}m.'.format(lat, lon, radius * 1000, center_lat,
                                                       center_lon, distance * 1000))
        else:
            distance = self.gps_distance_between_points(
                lat,
                lon,
                center_lat,
                center_lon)
            if distance > custom_radius.radius:
                raise exception_cls('GPS {0} {1} is more than {2} meters from the bypass target location {3}/{4}. '
                                    'Got {5}m.'.format(lat, lon, custom_radius.radius,
                                                       center_lat,
                                                       center_lon, distance * 1000))
        return True

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

    def image_file_url(self, obj_pk):
        """Generate an image url using a obj pk to uniquely identify an image.

        Keyword arguments:
        obj_pk: Name of the image file.
        """
        image_path = settings.MEDIA_URL
        url = os.path.join(image_path, obj_pk + '.jpg')
        return url

    def gps(self, direction, degrees, minutes):
        """Converts GPS degree/minutes to latitude or longitude."""
        dct = {'s': -1, 'e': 1}
        if direction not in dct.keys():
            raise TypeError('Direction must be one of {0}. Got {1}.'.format(dct.keys(), direction))
        d = float(degrees)
        m = float(minutes)
        return dct[direction] * round((d) + (m / 60), 5)

    def gps_lat(self, d, m):
        """Converts degree/minutes S to latitude."""
        return self.gps('s', d, m)

    def gps_lon(self, d, m):
        """Converts degree/minutes E to longitude."""
        return self.gps('e', d, m)
