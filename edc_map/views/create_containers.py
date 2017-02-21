from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SUB_SECTIONS, SECTIONS
from ..forms import ContainerSelectionForm
from ..models import Container
from ..site_mappers import site_mappers


class CreateContainers(EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    app_config_name = 'edc_map'
    template_name = 'edc_map/save_container.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def items(self, container_name=None):
        """Return  queryset of the item model.
        """
        value = self.kwargs.get(self.first_item_model_field, '')
        labels = []
        if container_name:
            try:
                container = Container.objects.get(container_name=container_name)
                labels = container.identifier_labels
            except Container.DoesNotExist:
                pass
        items = []
        map_area = self.kwargs.get('map_area', '')
        mapper = site_mappers.registry.get(map_area)
        if labels:
            qs_list = mapper.item_model.objects.filter(**{
                self.first_item_model_field: value,
                '{0}__in'.format(self.identifier_field_attr): labels})
        else:
            qs_list = mapper.item_model.objects.filter(**{
                self.first_item_model_field: value})
        for obj in qs_list:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 getattr(obj, self.identifier_field_attr)])
        return items

    def form_valid(self, form):
        set_inner_container = self.request.GET.get('set_inner_container')
        if form.is_valid():
            container_name = form.cleaned_data['container_name']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            items=self.items(container_name),
            set_inner_container=set_inner_container)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = self.request.GET.get('labels', '')
        set_container = self.request.GET.get('set_container')
        if labels:
            labels = labels.split(',')
        container_name = self.request.GET.get('container_name')
        container_boundry = self.request.GET.get('container')
        map_area = self.kwargs.get('map_area')
        polygon_points = []
        container_boundry = container_boundry.split('|')  # Container comes as a string pipe delimited.
        if container_boundry:
            del container_boundry[-1]
            for container_point in container_boundry:
                container_point = container_point.split(",")
                lat = float(container_point[0])
                lon = float(container_point[1])
                polygon_points.append([lat, lon])
        if container_name and map_area and polygon_points:
            self.create_container(container_name, map_area, labels, polygon_points)
        context.update(
            map_area='test_community',
            labels=labels,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            container_name=container_name,
            set_container=set_container)
        return context

    def create_container(self, container_name, map_area, labels, container_boundry):
        if labels:
            try:
                Container.objects.get(container_name=container_name)
            except Container.DoesNotExist:
                Container.objects.create(
                    labels=labels, container_name=container_name,
                    map_area=map_area, container_boundry=container_boundry)
