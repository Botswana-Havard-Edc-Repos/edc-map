from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from ..models import InnerContainer, Container
from ..site_mappers import site_mappers


class ItemCilentAllocationView(EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_map'
    first_item_model_field = 'map_area'
    identifier_field_attr = 'plot_identifier'
    template_name = 'edc_map/item_client_allocation.html'

    @property
    def containers(self):
        container_data = []
        containers = Container.objects.filter(
            map_area=site_mappers.current_map_area)
        for container in containers:
            container_data.append(
                [container.name, len(container.identifier_labels)])

    @property
    def inner_containers(self):
        container_data = []
        inner_containers = InnerContainer.objects.filter(
            map_area=site_mappers.current_map_area)
        for inner_container in inner_containers:
            container_data.append(
                [inner_container.name, len(inner_container.identifier_labels)])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            map_area=site_mappers.current_map_area)
        return context
