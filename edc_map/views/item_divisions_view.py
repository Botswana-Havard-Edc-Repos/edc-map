from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SUB_SECTIONS, SECTIONS
from ..forms import ContainerSelectionForm
from ..models import Container
from ..site_mappers import site_mappers


class ItemDivisionsView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'
    first_item_model_field = 'map_area'
    identifier_field_attr = 'plot_identifier'

    def divided_item_labels(self, container_name):
        try:
            item_labels = Container.objects.get(
                container_name=container_name).identifier_labels
        except Container.DoesNotExist:
            item_labels = []
        return item_labels

    @property
    def exisiting_containers(self):
        """Return a list of exisiting polygon.
        """
        containers = {}
        for container in Container.objects.all():
            container_name = container.container_name
            container = container.container_points
            if not containers.get(container_name):
                containers[container_name] = container
        return containers

    @property
    def ra_user(self):
        return ['ckgathi', 'tuser']

    def form_valid(self, form):
        set_inner_container = self.request.GET.get('set_inner_container')
        container_name = None
        if form.is_valid():
            container_name = form.cleaned_data['container_name']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            items=self.items(container_name),
            container_name=container_name,
            set_inner_container=set_inner_container)
        return self.render_to_response(context)

    def items(self, container_name=None):
        """Return  queryset of the item model.
        """
        value = self.kwargs.get(self.first_item_model_field, '')
        labels = []
        if container_name:
            try:
                item_division = Container.objects.get(container_name=container_name)
                labels = item_division.identifier_labels
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

    def get_context_data(self, **kwargs):
        context = super(ItemDivisionsView, self).get_context_data(**kwargs)
        set_innner_container = self.request.GET.get('set_innner_container')
        set_container = self.request.GET.get('set_container')
        map_area = self.kwargs.get('map_area', '')
        mapper = site_mappers.registry.get(map_area)
        context.update(
            items=self.items(),
            set_container=set_container,
            center_lat=mapper.center_lat,
            center_lon=mapper.center_lon,
            set_innner_container=set_innner_container,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            ra_user=self.ra_user,
            exisiting_containers=self.exisiting_containers)
        return context
