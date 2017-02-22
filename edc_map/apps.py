import os
import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.apps import apps as django_apps
from django.core.management.color import color_style

from edc_base.utils import get_utcnow

from .exceptions import FolderDoesNotExist


class AppConfig(DjangoAppConfig):
    name = 'edc_map'
    verbose_name = 'Edc Map'
    base_template_name = 'edc_base/base.html'
    image_folder = os.path.join(settings.MEDIA_ROOT, 'edc_map')
    app_label = 'edc_map'
    image_folder_url = os.path.join(settings.MEDIA_URL, 'edc_map')
    gps_file_name = '/Volumes/GARMIN/GPX/temp.gpx'
    gps_device = '/Volumes/GARMIN/'
    gpx_template = os.path.join(settings.STATIC_ROOT, 'edc_map/gpx/template.gpx')
    google_api_key = 'AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o'
    verify_point_on_save = True  # not used
    zoom_levels = ['16', '17', '18']

    # model that uses the landmark model mixin
    landmark_model = None  # ('bcpp_map', 'landmark')

    # model with the MapperModelMixin which has gps data fields
    mapper_model = None

    # uses the MapperDataModelMixin. This would be a replacement for the
    # mappers as classes
    mapp_data_model = None  # not used yet

    mapper_survey_model = None  # ('bcpp_interview', 'survey'), is this used??

    current_mapper_name = None

    @property
    def model_name(self):
        return 'plot'

    def ready(self):
        style = color_style()
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        sys.stdout.write(
            ' * using mapper model {}\n'.format(self.mapper_model))
        sys.stdout.write(
            ' * using survey model {}\n'.format(self.mapper_survey_model))
        from edc_map.signals import grep_google_map_image_on_post_save
        from edc_map.site_mappers import site_mappers
        if not os.path.exists(self.image_folder):
            raise FolderDoesNotExist(
                'Map Image folder for \'{name}\' does not exist. Got \'{folder}\'. '
                'See {name}.AppConfig.'.format(
                    name=self.name, folder=self.image_folder))
        site_mappers.autodiscover()
        if not self.current_mapper_name:
            try:
                self.current_mapper_name = settings.CURRENT_MAP_AREA
            except AttributeError:
                pass
        if self.current_mapper_name:
            site_mappers.load_current_mapper(
                site_mappers.get_mapper(self.current_mapper_name))
            sys.stdout.write(
                ' * current mapper is {}.\n'.format(
                    site_mappers.current_mapper.map_area))
        else:
            sys.stdout.write(
                style.ERROR(' * ERROR: current mapper not set.\n'))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
