import os
import sys

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.management.color import color_style


class AppConfig(DjangoAppConfig):
    name = 'edc_map'
    verbose_name = 'Edc Map'
    base_template_name = 'edc_base/base.html'
    image_folder = os.path.expanduser(
        os.path.join(settings.MEDIA_ROOT, 'edc_map'))
    app_label = 'edc_map'
    image_folder_url = os.path.join(settings.MEDIA_URL, 'edc_map')
    gps_file_name = '/Volumes/GARMIN/GPX/temp.gpx'
    gps_device = '/Volumes/GARMIN/'
    gpx_template = os.path.join(
        settings.STATIC_ROOT, 'edc_map/gpx/template.gpx')
    google_api_key = 'AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o'
    verify_point_on_save = True  # not used
    zoom_levels = ['16', '17', '18']

    # model that uses the landmark model mixin
    landmark_model = None  # ('bcpp_map', 'landmark')

    # model with the MapperModelMixin which has gps data fields
    mapper_model = None

    identifier_field_attr = None  # Identifier attribute used to query items.

    extra_filter_field_attr = None  # Extra filter boolean attribute name.

    current_mapper_name = None

    @property
    def model_name(self):
        return 'plot'

    @property
    def device_ids(self):
        try:
            device_ids = settings.EDC_MAP_DEVICE_IDS
        except AttributeError:
            device_ids = None
        return [d.strip() for d in (device_ids or '').split(',')]

    def ready(self):
        from edc_map.signals import grep_google_map_image_on_post_save
        from edc_map.site_mappers import site_mappers, SiteMapperError
        style = color_style()
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        sys.stdout.write(
            ' * using mapper model {}\n'.format(self.mapper_model))
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        site_mappers.autodiscover()
        try:
            site_mappers.current_map_area
        except SiteMapperError as e:
            sys.stdout.write(
                style.ERROR(f' * ERROR: Got {e}.\n'))
        else:
            sys.stdout.write(
                ' * current mapper is {}.\n'.format(
                    site_mappers.current_map_area))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))
