from django.apps import apps as django_apps

from ..models import Container, InnerContainer
from ..site_mappers import site_mappers


class StatisticsViewMixin:

    @property
    def identifier_field_attr(self):
        app_config = django_apps.get_app_config('edc_map')
        return app_config.identifier_field_attr

    @property
    def extra_filter_field_attr(self):
        app_config = django_apps.get_app_config('edc_map')
        return app_config.extra_filter_field_attr

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
