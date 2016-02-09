import os

try:
    # Django versions >= 1.9
    from urllib.request import urlretrieve
except ImportError:
    # Django versions < 1.9
    from urllib import urlretrieve

from time import sleep

from operator import itemgetter

from django.conf import settings

# from ..choices import ICONS
from ..exceptions import MapperError

LETTERS = list(map(chr, range(65, 91)))


class Snapshot(object):

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
        for lable, landmark_values in close_landmarks.items():
            if lable:
                markers_str += '&markers=color:blue%7Clabel:' + lable + '%7C' + str(landmark_values[2]) + ','
                markers_str += str(landmark_values[3])
        return markers_str

    def grep_image(self, url, image_name):
        """Grep a google map image and store in a location."""

        file_path = settings.MEDIA_ROOT
        image_path = os.path.join(file_path, image_name + '.jpg')
        if not os.path.exists(image_path):
            if os.path.exists(file_path):
                urlretrieve(url, image_path)
                sleep(2)
            else:
                raise MapperError("The path {0} provided does not exist.".format(file_path))

    def image_file_url(self, obj_pk):
        """Generate an image url using a obj pk to uniquely identify an image.

        Keyword arguments:
        obj_pk: Name of the image file.
        """
        image_path = settings.MEDIA_URL
        url = os.path.join(image_path, obj_pk + '.jpg')
        return url
