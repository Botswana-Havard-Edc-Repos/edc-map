from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_map.models import MapDivision
from django.contrib.auth.models import User

from ..constants import SECTIONS, SUB_SECTIONS


class HomeView(EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_map'
    template_name = 'edc_map/home.html'

    def update_sub_section(self, labels, sub_section_name, user, polygon):
        map_divisions = MapDivision.objects.filter(label__in=labels)
        for obj in map_divisions:
            obj.sub_section_polygon = polygon
            obj.sub_section_name = sub_section_name
            obj.user = user
            obj.save()

    def get(self, request, *args, **kwargs):
        super(HomeView, self).get(request, *args, **kwargs)
        labels = request.GET.get('labels')
        username = request.GET.get('user')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if labels:
            labels = labels.split(',')
        sub_section_name = request.GET.get('sub_section')
        polygon = request.GET.get('polygon')
        polygon_points = []
        if polygon:
            polygon = polygon.split('),(')
            for poly in polygon:
                poly = poly.split(',')
                print(poly, '-------------------------------')
                lat = poly[0].replace('(', '')
                lon = poly[1].replace(')', '')
                polygon_points.append([float(lat), float(lon)])
        if sub_section_name and labels and polygon and user:
            self.update_sub_section(labels, sub_section_name, user, polygon)
        context = self.get_context_data(**kwargs)
        context.update(
            labels=labels,
            sub_section_name=sub_section_name)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            map_area='test_community',
            sections=SECTIONS,
            sub_sections=SUB_SECTIONS)
        return context
