import os
import sys

from django.apps import AppConfig
from django.conf import settings

from edc_map.exceptions import FolderDoesNotExist


class EdcMapAppConfig(AppConfig):
    name = 'edc_map'
    verbose_name = 'Edc Map'
    image_folder = os.path.join(settings.MEDIA_ROOT, 'edc_map')
    image_folder_url = os.path.join(settings.MEDIA_URL, 'edc_map')
    google_api_key = 'AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o'
    verify_point_on_save = True  # not used
    zoom_levels = ['16', '17', '18']
    landmark_model = ('edc_map', 'landmark')
    mapper_data_model = ('edc_map', 'mapperdata')

    def ready(self):
        self.landmark_model = (self.name, 'landmark')
        self.mapper_data_model = (self.name, 'mapperdata')
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        from edc_map import signals
        from edc_map.site_mappers import site_mappers
        if not os.path.exists(self.image_folder):
            raise FolderDoesNotExist(
                'Map Image folder for \'{}\' does not exist. Got \'{}\'. See EdcMapAppConfig or subclass.'.format(
                    self.name, self.image_folder))
        site_mappers.autodiscover()
