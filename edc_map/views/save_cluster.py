from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_map.models import MapDivision


class SaveCluster(EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_map'
    template_name = 'edc_map/save_cluster.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(map_area='test_community')
        return context

    def create_section(self, section_name, map_area, labels, polygon):
        for label in labels:
            try:
                MapDivision.objects.get(label=label)
            except MapDivision.DoesNotExist:
                MapDivision.objects.create(
                    label=label, section_name=section_name,
                    map_area=map_area, section_polygon=polygon)

    def get(self, request, *args, **kwargs):
        super(SaveCluster, self).get(request, *args, **kwargs)
        labels = request.GET.get('labels')
        set_division = request.GET.get('set_division')
        if labels:
            labels = labels.split(',')
        section_name = request.GET.get('section_name')
        polygon = request.GET.get('polygon')
        map_area = self.kwargs.get('map_area')
        polygon_points = []
        if polygon:
            polygon = polygon.split('),(')
            for poly in polygon:
                poly = poly.split(',')
                lat = poly[0].replace('(', '')
                lon = poly[1].replace(')', '')
                polygon_points.append([float(lat), float(lon)])
        if section_name and map_area and polygon_points:
            self.create_section(section_name, map_area, labels, polygon)
        context = self.get_context_data(**kwargs)
        context.update(
            labels=labels,
            section_name=section_name,
            set_division=set_division)
        return self.render_to_response(context)
