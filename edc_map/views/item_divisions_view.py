import configparser
import os

from django.apps import apps as django_apps
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SUB_SECTIONS, SECTIONS
from ..forms import ContainerSelectionForm
from ..models import Container, InnerContainer
from ..site_mappers import site_mappers
from .statistics_view_mixin import StatisticsViewMixin
from edc_map.forms import CreateContainerForm


class ItemDivisionsView(StatisticsViewMixin, EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'

    def divided_item_labels(self, name):
        try:
            item_labels = Container.objects.get(
                name=name).identifier_labels
        except Container.DoesNotExist:
            item_labels = []
        return item_labels

    @property
    def exisiting_containers(self):
        """Return a dictionary of exisiting polygon.
        """
        return {obj.name: obj.points for obj in Container.objects.filter(
            map_area=site_mappers.current_map_area)}

    @property
    def device_ids(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(settings.ETC_DIR, settings.CONFIG_FILE))
        return sorted(config['deployment'].get('device_ids').split(','))

    def form_valid(self, form):
        if form.is_valid():
            name = form.cleaned_data['container_name']
            type_container = self.request.GET.get('set_inner_container')
            context = self.get_context_data(**self.kwargs)
            context.update(
                form=form,
                items=self.items(name, type_container),
                container_name=name,
                set_inner_container=type_container)
        return self.render_to_response(context)

    def inner_container_labels(self, name):
        """Return a list of labels for a given container.
        """
        labels = []
        inner_containers = InnerContainer.objects.filter(
            container__name=name,
            map_area=site_mappers.current_map_area)
        if inner_containers:
            for inner_container in inner_containers:
                labels.extend(inner_container.identifier_labels)
        return labels

    def contained_labels(self, name):
        """Return a list of labels for container given.
        """
        current_contained_labels = []
        try:
            container = Container.objects.get(
                name=name, map_area=site_mappers.current_map_area)
            current_contained_labels = container.identifier_labels
        except Container.DoesNotExist:
            pass
        return current_contained_labels

    def items(self, name=None, container_type=None, extra_filter_field_value=None):
        """Return  queryset of the item model.
        """
        labels = []  # Labels to exclude when creating a container.
        containers = Container.objects.filter(
            map_area=site_mappers.current_map_area)
        for container in containers:
            labels.extend(container.identifier_labels)
        contained_labels = self.contained_labels(name)

        items = []
        exclude_labels = self.inner_container_labels(name)
        mapper = site_mappers.registry.get(site_mappers.current_map_area)
        qs = []
        if extra_filter_field_value == 'Yes':
            extra_filter_field_value = [True]
        elif extra_filter_field_value == 'No':
            extra_filter_field_value = [False]
        elif extra_filter_field_value == 'All':
            extra_filter_field_value = [True, False]
        if container_type == 'set_container':  # QuerySet  to create a container
            qs = mapper.item_model.objects.filter(**{
                'map_area': site_mappers.current_map_area,
                '{0}__in'.format(self.extra_filter_field_attr): extra_filter_field_value}).exclude(**{'{0}__in'.format(self.identifier_field_attr): labels})
        elif container_type == 'set_inner_container' and container:
            #  QuerySet  to create an Inner container.
            qs = mapper.item_model.objects.filter(**{
                'map_area': site_mappers.current_map_area,
                '{0}__in'.format(self.identifier_field_attr): contained_labels}).exclude(**{
                    '{0}__in'.format(self.identifier_field_attr): exclude_labels})
        for obj in qs:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 getattr(obj, self.identifier_field_attr)])
        return items

    def get_context_data(self, **kwargs):
        context = super(ItemDivisionsView, self).get_context_data(**kwargs)
        set_inner_container = self.request.GET.get('set_inner_container')
        container_type = self.request.GET.get('set_container')
        mapper = site_mappers.registry.get(site_mappers.current_map_area)
        if self.request.method == 'POST':
            create_container_form = CreateContainerForm(self.request.POST)
            if create_container_form.is_valid():
                extra_filter_field_value = create_container_form.data[
                    'extra_filter_field_attr']
                items = self.items(
                    container_type=container_type,
                    extra_filter_field_value=extra_filter_field_value)
                context.update(items=items)

        context.update(
            set_container=container_type,
            map_area=site_mappers.current_map_area,
            center_lat=mapper.center_lat,
            create_container_form=create_container_form,
            center_lon=mapper.center_lon,
            set_inner_container=set_inner_container,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            device_ids=self.device_ids,
            exisiting_containers=self.exisiting_containers,
            sectioning_statistics=self.sectioning_statistics)
        return context
