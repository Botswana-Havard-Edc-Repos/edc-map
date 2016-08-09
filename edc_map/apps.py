import os
import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings

from edc_map.exceptions import FolderDoesNotExist


class AppConfig(DjangoAppConfig):
    name = 'edc_map'
    verbose_name = 'Edc Map'
    image_folder = os.path.join(settings.MEDIA_ROOT, 'edc_map')
    image_folder_url = os.path.join(settings.MEDIA_URL, 'edc_map')
    google_api_key = 'AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o'
    verify_point_on_save = True  # not used
    zoom_levels = ['16', '17', '18']

    # model that uses the landmark model mixin
    landmark_model = None  # ('bcpp_map', 'landmark')

    # model with the MapperModelMixin which has gps data fields
    mapper_model = None  # ('bcpp_interview', 'subjectlocation')

    # uses the MapperDataModelMixin. This would be a replacement for the mappers as classes
    mapp_data_model = None  # not used yet

    mapper_survey_model = None  # ('bcpp_interview', 'survey'), is this used??

    def ready(self):
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        from edc_map import signals
        from edc_map.site_mappers import site_mappers
        if not os.path.exists(self.image_folder):
            raise FolderDoesNotExist(
                'Map Image folder for \'{name}\' does not exist. Got \'{folder}\'. '
                'See {name}.AppConfig.'.format(name=self.name, folder=self.image_folder))
        site_mappers.autodiscover()
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
