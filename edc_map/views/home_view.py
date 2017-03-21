from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SECTIONS, SUB_SECTIONS
from ..exceptions import MapperError
from ..forms import ContainerSelectionForm
from ..models import InnerContainer, Container
from ..site_mappers import site_mappers


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    app_config_name = 'edc_map'
    first_item_model_field = 'map_area'
    identifier_field_attr = 'plot_identifier'
    template_name = 'edc_map/home.html'

    @property
    def sectioning_statistics(self):
        """Return statistics of sectioning items."""

        contained_items = []
        for container in Container.objects.filter(
                map_area=site_mappers.current_map_area):
            contained_items.extend(container.identifier_labels)
        total_container_items = len(contained_items)

        #  Items in inner containers.
        inner_contained_items = []
        for inner_container in InnerContainer.objects.filter(
                container__map_area=site_mappers.current_map_area):
            inner_contained_items.extend(inner_container.identifier_labels)
        total_inner_contained_items = len(inner_contained_items)

        #  Items not in any container.
        mapper = site_mappers.registry.get(site_mappers.current_map_area)
        total_items_not_contained = mapper.item_model.objects.filter(**{
            'map_area': site_mappers.current_map_area}).exclude(**{
                '{0}__in'.format(
                    self.identifier_field_attr): contained_items}).count()

        #  Items in a container but not in any inner container.
        items_not_in_inner_container = list(
            set(contained_items) - set(inner_contained_items))

        return [
            total_container_items,
            total_inner_contained_items,
            total_items_not_contained,
            len(items_not_in_inner_container)]

    @property
    def containers_items(self):
        items_list = []
        for container in Container.objects.filter(
                map_area=site_mappers.current_map_area):
            items_list += container.identifier_labels
        return items_list

    @property
    def inner_containers_items(self):
        items_list = []
        for inner_container in InnerContainer.objects.filter(
                container__map_area=site_mappers.current_map_area):
            items_list.extend(inner_container.identifier_labels)
        return items_list

    @property
    def items_not_contained(self):
        mapper = site_mappers.registry.get(site_mappers.current_map_area)
        qs_list = mapper.item_model.objects.filter(**{
            self.first_item_model_field: site_mappers.current_map_area}).exclude(**{
                '{0}__in'.format(self.identifier_field_attr): self.containers_items})
        return qs_list.count()

    @property
    def containers_items_not_ininner_contained(self):
        return list(set(self.containers_items) -
                    set(self.inner_containers_items))

    def create_inner_container(
            self, labels, name, device_id, boundry, container):
        try:
            InnerContainer.objects.get(
                name=name, map_area=site_mappers.current_map_area)
        except InnerContainer.DoesNotExist:
            InnerContainer.objects.create(
                device_id=device_id,
                boundry=boundry,
                container=container,
                name=name,
                map_area=site_mappers.current_map_area,
                labels=labels)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        context = self.get_context_data(**self.kwargs)
        context['form'] = form
        return super(HomeView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def labels(self):
        """Returns a patients queryset after pagination."""
        labels = self.request.GET.get('labels', [])
        if labels:
            labels = labels.split(',')
        return labels

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = self.request.GET.get('device_id')
        inner_container_name = self.request.GET.get('inner_container_name')
        inner_container = self.request.GET.get('inner_container')
        name = self.request.GET.get('container_name')
        polygon_points = []
        labels = self.request.GET.get('labels', [])
        if labels:
            labels = labels.split(',')
        if inner_container:
            inner_container = inner_container.split('|')  # Container comes as a string pipe delimited.
            if inner_container:
                del inner_container[-1]
                for inner_container_point in inner_container:
                    inner_container_point = inner_container_point.split(",")
                    lat = float(inner_container_point[0])
                    lon = float(inner_container_point[1])
                    polygon_points.append([lat, lon])
        if name:
            try:
                container = Container.objects.get(name=name)
            except Container.DoesNotExist:
                raise MapperError("Inner container can not exist without a container.")
        if inner_container_name and labels and polygon_points and device_id:
            self.create_inner_container(
                labels,
                inner_container_name,
                device_id,
                polygon_points,
                container)
        context.update(
            map_area=site_mappers.current_map_area,
            labels=self.labels,
            inner_container_name=inner_container_name,
            container_name=name,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            sectioning_statistics=self.sectioning_statistics)
        return context
