from django.apps import AppConfig


class EdcMapAppConfig(AppConfig):
    name = 'edc_map'
    verbose_name = 'Edc Map'

    def ready(self):
        from edc_map import signals
        from edc_map.site_mappers import site_mappers
        site_mappers.autodiscover()
