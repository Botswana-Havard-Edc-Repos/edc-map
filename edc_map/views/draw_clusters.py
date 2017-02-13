from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from ..models import MapDivision
from edc_map.site_mappers import site_mappers

from ..constants import SUB_SECTIONS, SECTIONS


class DrawClusterMixin(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'
    first_item_model_field = 'map_area'
    second_item_model_field = 'plot_identifier'

    def clustred_item_identifiers(self, section_name):
        cluster_labels = []
        for division in MapDivision.objects.filter(section_name=section_name):
            cluster_labels.append(division.label)
        return cluster_labels

    @property
    def exisiting_section_polygon(self):
        """Return a list of exisiting polygon."""
        sectoin_polygons = {}
        for map_division in MapDivision.objects.all():
            section_name = map_division.section_name
            polygon = map_division.section_polygon
            formated_polygon = []
            if polygon:
                polygon = polygon.replace('[', '')
                polygon = polygon.replace(']', '')
                polygon = polygon.replace('(', '')
                polygon = polygon.replace(')', '')
#                 polygon = polygon.split('\", \"')
                for poly in polygon:
                    print(poly, '*&^%%%%$#@!@#$$%')
                    poly = poly.split(',')
                    lat = float(poly[0].replace('\"', ''))
                    lon = float(poly[1].replace('\"', ''))
                    formated_polygon.append([lat, lon])
            if not sectoin_polygons.get(section_name):
                sectoin_polygons[section_name] = formated_polygon
        return sectoin_polygons

    @property
    def ra_user(self):
        return ['ckgathi', 'tuser']

    def get(self, request, *args, **kwargs):
        super(DrawClusterMixin, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        set_sub_section = request.GET.get('set_sub_section')
        set_section = request.GET.get('set_section')
        context.update(
            set_section=set_section,
            items=self.get_objects(request),
            set_sub_section=set_sub_section)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        super(DrawClusterMixin, self).get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        set_sub_section = request.GET.get('set_sub_section')
        context.update(
            items=self.get_objects(request),
            set_sub_section=set_sub_section)
        return self.render_to_response(context)

    def get_objects(self, request):
        """Return  queryset of the item model."""
        value = self.kwargs.get(self.first_item_model_field, '')
        section_name = request.POST.get('section_name')
        labels = self.clustred_item_identifiers(section_name)
        items = []
        map_area = self.kwargs.get('map_area', '')
        self.mapper = site_mappers.registry.get(map_area)
        obj_list = self.mapper.item_model.objects.filter(**{
            self.first_item_model_field: value, '{0}__in'.format(self.second_item_model_field): labels})
        for obj in obj_list:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 obj.plot_identifier])
        return items

    def get_context_data(self, **kwargs):
        context = super(DrawClusterMixin, self).get_context_data(**kwargs)
        context.update(
            sections=SECTIONS,
            sub_sections=SUB_SECTIONS,
            ra_user=self.ra_user,
            exisiting_section_polygon=self.exisiting_section_polygon)
        return context
