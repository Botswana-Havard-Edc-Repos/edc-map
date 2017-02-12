from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from ..models import MapDivision
from edc_map.site_mappers import site_mappers


class DrawClusterMixin(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'
    first_item_model_field = 'map_area'
    second_item_model_field = 'plot_identifier'

    def clustred_items(self):
        cluster_labels = []
        for section in MapDivision.objects.all():
            cluster_labels.append(section.label)
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
                polygon = polygon.split('\", \"')
                for poly in polygon:
                    poly = poly.split(',')
                    lat = float(poly[0].replace('\"', ''))
                    lon = float(poly[1].replace('\"', ''))
                    formated_polygon.append([lat, lon])
            if not sectoin_polygons.get(section_name):
                sectoin_polygons[section_name] = formated_polygon
        return sectoin_polygons

    @property
    def sections(self):
        """Return a list of sections."""
        return ['A', 'B', 'C', 'D', 'E']

    @property
    def sub_sections(self):
        """Return a list of sub sections."""
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

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
            set_sub_section=set_sub_section)
        return self.render_to_response(context)

    @property
    def get_objects(self):
        """Return  queryset of the item model."""
        value = self.kwargs.get(self.first_item_model_field, '')
        value_list = self.kwargs.get(self.second_item_model_field, [])
        items = []
        map_area = self.kwargs.get('map_area', '')
        self.mapper = site_mappers.registry.get(map_area)
        obj_list = self.mapper.item_model.objects.filter(**{
            self.first_item_model_field: value}).exclude(**{
                '{0}__in'.format(self.second_item_model_field): value_list})
        for obj in obj_list:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 obj.plot_identifier])
        return items

    def get_context_data(self, **kwargs):
        context = super(DrawClusterMixin, self).get_context_data(**kwargs)
        context.update(
            items=self.get_objects,
            sections=self.sections,
            sub_sections=self.sub_sections,
            ra_user=self.ra_user,
            exisiting_section_polygon=self.exisiting_section_polygon)
        return context
