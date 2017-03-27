from collections import OrderedDict

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from ..models import InnerContainer, Container
from ..site_mappers import site_mappers
from .statistics_view_mixin import StatisticsViewMixin


class ItemCilentAllocationView(StatisticsViewMixin, EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_map'
    template_name = 'edc_map/item_client_allocation.html'

    @property
    def cotainer_data(self):
        """Return a dictionary of containers.
        """
        return OrderedDict(sorted({obj.name: len(
            obj.identifier_labels) for obj in Container.objects.filter(
            map_area=site_mappers.current_map_area)}.items()))

    @property
    def inner_cotainer_data(self):
        """Return a dictionary of inner containers.
        """
        inner_cotainer_data = [[
            obj.device_id,
            obj.container.name,
            obj.name,
            len(obj.identifier_labels)
        ] for obj in InnerContainer.objects.filter(
            map_area=site_mappers.current_map_area)]
        inner_cotainer_data = sorted(inner_cotainer_data, key=lambda element: (element[1], element[2]))
        return inner_cotainer_data

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            map_area=site_mappers.current_map_area,
            cotainer_data=self.cotainer_data,
            inner_cotainer_data=self.inner_cotainer_data,
            sectioning_statistics=self.sectioning_statistics)
        return context
