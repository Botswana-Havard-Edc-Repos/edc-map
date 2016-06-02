import os

from collections import OrderedDict
from time import sleep
from urllib.parse import urlencode
from urllib.request import urlretrieve
from geopy import Point
from django.apps import apps as django_apps
from django.conf import settings

from .geo_mixin import GeoMixin
from .site_mappers import site_mappers
from .exceptions import FolderDoesNotExist
from .mapper import LANDMARK_NAME, LONGITUDE, LATITUDE
from edc_map.structures import Landmark

DISTANCE = 3

LETTERS = list(map(chr, range(65, 91)))


class Snapshot(GeoMixin):

    google_api_url = 'http://maps.google.com/maps/api/staticmap'
    app_label = 'edc_map'

    def __init__(self, filename_prefix, point, map_area,
                 zoom_levels=None, app_label=None):
        """
        Keyword arguments:
            filename_prefix: a unique string prefix, e.g. a model pk.
            point: (latitude, longitude).
            map_area: name of area and also the reference key to the mapper for the area, e.g community
            zoom_levels: a list of zomm levels (Optional)
        """
        self.app_config = django_apps.get_app_config(app_label or self.app_label)
        self.zoom_levels = zoom_levels or ['16', '17', '18']
        try:
            self.image_folder = settings.EDC_MAP_FOLDER
        except AttributeError:
            self.image_folder = os.path.join(settings.MEDIA_ROOT, 'edc_map')
        if not os.path.exists(self.image_folder):
            raise FolderDoesNotExist(
                'Map Image folder for edc_map does not exist. Got {}'.format(self.image_folder))
        self.filename_prefix = filename_prefix  # used for unique filename
        self.map_area = map_area
        self.point = point or Point(0.0, 0.0)
        self.mapper = site_mappers.get_mapper(map_area.lower())
        self.landmarks = self.prepare_landmarks(self.mapper.landmarks)

    def retrieve_image_result_handler(self, result):
        """Callback to handle the result from each urlretrieve."""
        return None

    def retrieve_image_reporthook(self, block_number, read_size, total_size):
        """Callback for urlretrieve reporthook."""
        pass

    @property
    def image_filenames(self):
        """Return a dictionary of filenames, key by zoom level."""
        image_filenames = {}
        for zoom_level in self.zoom_levels:
            image_filenames.update({
                zoom_level: str(self.filename_prefix) + str(zoom_level) + '.jpg'})
        return image_filenames

    def image_filename(self, zoom_level):
        """Return an image filename."""
        return str(self.filename_prefix) + str(zoom_level) + '.jpg'

    def retrieve_and_store_images(self):
        """Retrieve and store images for each zoom level."""
        image_filenames = []
        for zoom_level in self.zoom_levels:
            path, _ = self.retrieve_and_store_image(zoom_level)
            image_filenames.append(path)
        return image_filenames

    def retrieve_and_store_image(self, zoom_level):
        """Retrieve and store image for this zoom level"""
        image_file_name = os.path.join(self.image_folder, self.image_filename(zoom_level))
        result = (image_file_name, None)
        if not os.path.exists(image_file_name):
            result = urlretrieve(
                self.image_url(zoom_level),
                image_file_name,
                reporthook=self.retrieve_image_reporthook)
            sleep(2)
        self.retrieve_image_result_handler(result)
        return result

    def image_url(self, zoom_level):
        """Return the url of the google map image."""
        markers = self.format_as_markers(self.point, color='red')
        query_string = urlencode(
            OrderedDict(
                center=str(self.point.latitude) + ',' + str(self.point.longitude),
                format='png32',
                key=self.app_config.google_api_key,
                maptype='satellite',
                scale='2',
                sensor='false',
                size='640x600',
                zoom=zoom_level))
        query_string += '&' + '&'.join([markers] + self.landmarks_as_markers)
        return self.google_api_url + '?' + query_string

    @property
    def landmarks_by_label(self):
        """Returns an ordered dict of label: landmark."""
        return OrderedDict(zip(LETTERS, self.landmarks))

    @property
    def landmarks_as_markers(self):
        """Return a list of landmarks formatted/encoded as markers."""
        markers = []
        color = 'blue'
        for label, landmark in self.landmarks_by_label.items():
            markers.append(
                self.format_as_markers(landmark.point, label=label, color=color))
        return markers

    def prepare_landmarks(self, mapper_landmarks):
        """Return mapper landmarks as a list of namedtuples (adds distance from target)."""
        landmarks = []
        for landmark in mapper_landmarks:
            landmark = Landmark(landmark[LANDMARK_NAME], Point(landmark[LATITUDE], landmark[LONGITUDE]), 0)
            distance = self.distance_between_points(self.point, landmark.point)
            landmark = Landmark(landmark.name, landmark.point, distance)
            landmarks.append(landmark)
        landmarks = sorted(landmarks, key=lambda x: x.distance)
        return tuple(landmarks)

    def format_as_markers(self, point, color, label=None):
        """Format and encode as a markers parameter."""
        template = 'color:{color}|label:{label}|{longitude},{latitude}'
        if not label:
            # not sure why, but need to flip lat and lon for the center point??
            template = 'color:{color}|{latitude},{longitude}'
        string = template.format(
            color=color, label=label, latitude=point.latitude, longitude=point.longitude)
        return urlencode({'markers': string}, encoding='utf-8')
