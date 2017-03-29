from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SUB_SECTIONS, SECTIONS
from ..forms import ContainerSelectionForm, CreateContainerForm
from ..models import Container
from ..site_mappers import site_mappers
from .statistics_view_mixin import StatisticsViewMixin


class CreateContainers(StatisticsViewMixin, EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    app_config_name = 'edc_map'
    template_name = 'edc_map/save_container.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def items(self, name=None):
        """Return  queryset of the item model.
        """
        labels = []
        if name:
            try:
                container = Container.objects.get(name=name)
                labels = container.identifier_labels
            except Container.DoesNotExist:
                pass
        items = []
        mapper = site_mappers.registry.get(site_mappers.current_map_area)
        qs = []
        if labels:
            qs = mapper.item_model.objects.filter(**{
                'map_area': site_mappers.current_map_area,
                '{0}__in'.format(self.identifier_field_attr): labels})
        else:
            qs = mapper.item_model.objects.filter(**{
                'map_area': site_mappers.current_map_area})
        for obj in qs:
            items.append(
                [float(obj.gps_target_lat),
                 float(obj.gps_target_lon),
                 getattr(obj, self.identifier_field_attr)])
        return items

    def form_valid(self, form):
        set_inner_container = self.request.GET.get('set_inner_container')
        if form.is_valid():
            name = form.cleaned_data['container_name']
        context = self.get_context_data(**self.kwargs)
        context.update(
            form=form,
            items=self.items(name),
            set_inner_container=set_inner_container)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_container = self.request.GET.get('set_container')
        name = self.request.GET.get('container_name')
        boundry = self.request.GET.get('boundry')
        labels = self.request.GET.get('labels', '')
        create_container_form = CreateContainerForm()
        container_created = False
        if name and boundry:
            container_created = self.create_container(name, labels, boundry)
        if labels and container_created:
            labels = labels.split(',')
        elif labels and not container_created:
            labels = []
        context.update(
            map_area=site_mappers.current_map_area,
            labels=labels,
            create_container_form=create_container_form,
            container_created=container_created,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            container_name=name,
            set_container=set_container,
            sectioning_statistics=self.sectioning_statistics)
        return context

    def create_container(self, name, labels, boundry):
        container_created = False
        if labels:
            try:
                Container.objects.get(
                    name=name, map_area=site_mappers.current_map_area)
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    'The Container {0} already exists in {1}'.format(name, site_mappers.current_map_area))
            except Container.DoesNotExist:
                Container.objects.create(
                    labels=labels, name=name,
                    map_area=site_mappers.current_map_area, boundry=boundry)
                container_created = True
        return container_created
