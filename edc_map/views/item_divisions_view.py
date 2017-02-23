from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SUB_SECTIONS, SECTIONS
from ..forms import ContainerSelectionForm
from ..models import Container, InnerContainer
from ..site_mappers import site_mappers


class ItemDivisionsView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'
    first_item_model_field = 'map_area'
    identifier_field_attr = 'plot_identifier'

    def divided_item_labels(self, name):
        try:
            item_labels = Container.objects.get(
                name=name).identifier_labels
        except Container.DoesNotExist:
            item_labels = []
        return item_labels

    @property
    def exisiting_containers(self):
        """Return a list of exisiting polygon.
        """
        containers = {}
        for container in Container.objects.all():
            name = container.name
            points = container.points
            if not containers.get(name):
                containers[name] = points
        return containers

    @property
    def ra_user(self):
        usernames = []
        for user in User.objects.filter(groups__name__in=['RA']):
            usernames.append(user.username)
        return usernames

    def form_valid(self, form):
        type_container = self.request.GET.get('set_inner_container')
        if form.is_valid():
            name = form.cleaned_data['container_name']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            items=self.items(name, type_container),
            container_name=name,
            set_inner_container=type_container)
        return self.render_to_response(context)

    def inner_container_labels(self, container_name):
        labels = []
        try:
            inner_containers = InnerContainer.objects.filter(container__name=container_name)
            for inner_container in inner_containers:
                labels = labels + inner_container.identifier_labels
        except InnerContainer.DoesNotExist:
            pass
        return labels

    def items(self, name=None, container_type=None):
        """Return  queryset of the item model.
        """
        value = self.kwargs.get(self.first_item_model_field, '')
        labels = []
        containers = Container.objects.all().exclude(name=name)
        for container in containers:
            labels += container.identifier_labels
        container = None
        current_container_labels = []
        try:
            container = Container.objects.get(name=name)
            current_container_labels = container.identifier_labels
        except Container.DoesNotExist:
            pass
        items = []
        exclude_labels = self.inner_container_labels(name)
        map_area = self.kwargs.get('map_area', '')
        mapper = site_mappers.registry.get(map_area)
        qs_list = []
        if labels and container_type == 'set_container':
            qs_list = mapper.item_model.objects.filter(**{
                self.first_item_model_field: value}).exclude(**{
                    '{0}__in'.format(self.identifier_field_attr): labels})
        elif container_type == 'set_inner_container' and container:
            qs_list = mapper.item_model.objects.filter(**{
                self.first_item_model_field: value,
                '{0}__in'.format(self.identifier_field_attr): current_container_labels}).exclude(**{
                    '{0}__in'.format(self.identifier_field_attr): exclude_labels})
        for obj in qs_list:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 getattr(obj, self.identifier_field_attr)])
        return items

    def get_context_data(self, **kwargs):
        context = super(ItemDivisionsView, self).get_context_data(**kwargs)
        set_inner_container = self.request.GET.get('set_inner_container')
        set_container = self.request.GET.get('set_container')
        map_area = self.kwargs.get('map_area', '')
        mapper = site_mappers.registry.get(map_area)
        context.update(
            items=self.items(container_type=set_container),
            set_container=set_container,
            center_lat=mapper.center_lat,
            center_lon=mapper.center_lon,
            set_inner_container=set_inner_container,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            ra_user=self.ra_user,
            exisiting_containers=self.exisiting_containers)
        return context
