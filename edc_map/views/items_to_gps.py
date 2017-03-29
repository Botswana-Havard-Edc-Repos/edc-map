import os

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.apps import apps as django_apps

from edc_base.view_mixins import EdcBaseViewMixin

from ..site_mappers import site_mappers
from ..exceptions import MapperError
from ..models import InnerContainer


class ItemsToGps(EdcBaseViewMixin, TemplateView):
    """Create a .gpx file to store coordinates in the GPS receiver.
    """
    template_name = 'edc_map/items_to_gps.html'
    app_label = 'edc_map'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def identifier_field_attr(self):
        app_config = django_apps.get_app_config('edc_map')
        return app_config.identifier_field_attr

    @property
    def item_identifiers(self):
        edc_device_app_config = django_apps.get_app_config('edc_device')
        device_id = edc_device_app_config.device_id
        try:
            inner_containers = InnerContainer.objects.get(
                map_area=site_mappers.current_map_area, device_id=device_id)
            return inner_containers.identifier_labels
        except InnerContainer.DoesNotExist:
            return []
        return []

    def items(self, map_area):
        """Return a list of items."""
        qs = None
        mapper = site_mappers.registry.get(map_area)
        if self.item_identifiers:
            qs = mapper.item_model.objects.filter(**{
                'map_area': site_mappers.current_map_area,
                '{0}__in'.format(self.identifier_field_attr): self.item_identifiers})
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = None
        items = self.items(site_mappers.current_map_area)
        gps_device = django_apps.get_app_config(self.app_label).gps_device
        gps_file_name = django_apps.get_app_config(self.app_label).gps_file_name
        gpx_template = django_apps.get_app_config(self.app_label).gpx_template
        if items:
            if os.path.exists(gps_device):
                if os.path.exists(gps_file_name):
                    os.remove(gps_file_name)
                if not os.path.exists(gpx_template):
                    raise MapperError(
                        'xml template file for GPS device does not exist, '
                        'either run collectstatic or check if the file exists')
                f = open(gpx_template, 'r')
                line = f.readline()
                lines = f.read()
                f.close()
                wf = open(gps_file_name, 'a')
                wf.write(line)
                for item in items:
                    identifier_name = str(
                        getattr(item, self.identifier_field_attr))
                    lat = item.gps_target_lat
                    lon = item.gps_target_lon
                    ele = 0.0
                    city_village = site_mappers.current_map_area
                    str_from_edc = '<wpt lat="' + str(lat) + '" lon="' + str(lon) + '"><ele>' + str(ele) + '</ele>' + '<name>' + str(identifier_name) + '</name><extensions><gpxx:WaypointExtension><gpxx:Address><gpxx:City>' + str(city_village) + '</gpxx:City><gpxx:State>South Eastern</gpxx:State></gpxx:Address></gpxx:WaypointExtension></extensions>' + '</wpt>'
                    wf.write(str_from_edc)
                wf.write(lines)
                wf.close()
                message = 'Items Succefully loaded to a GPS device.'
            else:
                message = 'Gps device not mounted'
        context.update(
            map_area=site_mappers.current_map_area,
            message=message)
        return context
