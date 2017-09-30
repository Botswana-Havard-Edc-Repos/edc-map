from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from ..models import InnerContainer
from ..site_mappers import site_mappers
from .statistics_view_mixin import StatisticsViewMixin


class ItemListView(StatisticsViewMixin, EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_map'
    template_name = 'edc_map/item_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def item_list(self, container_name=None, inner_container_name=None, device_id=None):
        """Return a list of items."""
        item_list = []
        try:
            item_list = InnerContainer.objects.get(
                map_area=site_mappers.current_map_area,
                container__name=container_name,
                name=inner_container_name,
                device_id=device_id).identifier_labels
        except InnerContainer.DoesNotExist:
            item_list = []
        return item_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        container_name = kwargs.get('container_name', None)
        device_id = kwargs.get('device_id', None)
        inner_container_name = kwargs.get('inner_container_name', None)
        context.update(
            map_area=site_mappers.current_map_area,
            sectioning_statistics=self.sectioning_statistics,
            item_list=self.item_list(
                container_name=container_name,
                inner_container_name=inner_container_name,
                device_id=device_id),
            device_id=device_id,
            container_name=container_name,
            inner_container_name=inner_container_name,)
        return context
