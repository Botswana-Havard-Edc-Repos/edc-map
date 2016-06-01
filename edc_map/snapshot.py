import os

from operator import itemgetter
from time import sleep
from urllib.request import urlretrieve

from django.conf import settings

from .geo_mixin import GeoMixin
from .site_mappers import site_mappers

LETTERS = list(map(chr, range(65, 91)))


class FolderDoesNotExist(Exception):
    pass


class Snapshot(GeoMixin):

    def __init__(self, filename_prefix, latitude, longitude, map_area, zoom_levels=None):
        """
        Keyword arguments:
            coordinates: a list of coordinates pair, e.g [latitude, longitude].
            landmarks: a list of a list of landmarks, e.g [[landmark_name, latitude, longitude],].
        """
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
        self.latitude, self.longitude = latitude or 0.0, longitude or 0.0
        self.mapper = site_mappers.get_mapper(map_area)
        self.landmarks = self.mapper.landmarks

    def retrieve_image_result_handler(self, result):
        """Callback to handle the result from each urlretrieve."""
        return None

    def retrieve_image_reporthook(self, blocknumber, read_size, total_size):
        pass

    @property
    def image_filenames(self):
        image_filenames = {}
        for zoom_level in self.zoom_levels:
            image_filenames.update({
                zoom_level: str(self.filename_prefix) + str(zoom_level) + '.jpg'})
        return image_filenames

    def image_filename(self, zoom_level):
        return str(self.filename_prefix) + str(zoom_level) + '.jpg'

    def retrieve_and_store_images(self):
        """Generate and store images for each zoom level."""
        image_filenames = []
        for zoom_level in self.zoom_levels:
            path, _ = self.retrieve_and_store_image(zoom_level)
            image_filenames.append(path)
        return image_filenames

    def retrieve_and_store_image(self, zoom_level):
        """Retrieve and store image for this zoom level"""
        image_file_name = self.image_name(zoom_level)
        image_url = self.google_image_url(zoom_level)
        if not os.path.exists(image_file_name):
            result = urlretrieve(image_url, image_file_name, reporthook=self.urlretrieve_reporthook)
            sleep(2)
        self.retrieve_image_result_handler(result)
        return result

    def google_image_url(self, zoom_level):
        """Return the url of a google map image."""
        url = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32'
        url += '&zoom=' + str(zoom_level) + '&center=' + str(self.latitude) + ',' + str(self.longitude)
        url += self.landmarks_url + '&markers=color:red%7C' + str(self.latitude) + ','
        url += str(self.longitude) + '&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o&sensor=false'
        return url

    @property
    def nearby_landmarks(self):
        """Return landmarks sorted by close distance to the target location.
        """
        distance_landmarks = []
        landmarks_dictionary = {}
        if self.landmarks:
            for landmark in self.landmarks:
                distance = self.gps_distance_between_points(
                    self.latitude, self.longitude, landmark[1], landmark[2])
                distance_landmarks.append([distance, landmark[0], landmark[1], landmark[2]])
            landmarks = sorted(distance_landmarks, key=itemgetter(0))
            landmarks_dictionary = dict(zip(LETTERS, landmarks))
        return landmarks_dictionary

    @property
    def landmarks_url(self):
        """Return url for landmarks to add to google map image url."""
        landmarks_url = ''
        for label, landmark_values in self.nearby_landmarks.items():
            if label:
                landmarks_url += '&markers=color:blue%7Clabel:' + label + '%7C' + str(landmark_values[2]) + ','
                landmarks_url += str(landmark_values[3])
        return landmarks_url
