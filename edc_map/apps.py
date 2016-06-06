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
    verify_point_on_save = True

    def ready(self):
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        from edc_map import signals
        from edc_map.site_mappers import site_mappers
        if not os.path.exists(self.image_folder):
            raise FolderDoesNotExist(
                'Map Image folder for \'{}\' does not exist. Got \'{}\''.format(
                    self.name, self.image_folder))
        site_mappers.autodiscover()
