from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..constants import SECTIONS, SUB_SECTIONS
from ..exceptions import MapperError
from ..forms import ContainerSelectionForm, CreateContainerForm
from ..models import InnerContainer, Container
from ..site_mappers import site_mappers
from .statistics_view_mixin import StatisticsViewMixin


class HomeView(StatisticsViewMixin, EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    app_config_name = 'edc_map'
    template_name = 'edc_map/home.html'

    def create_inner_container(
            self, labels, name, device_id, boundry, container):
        inner_container_created = False
        try:
            InnerContainer.objects.get(
                name=name,
                map_area=site_mappers.current_map_area,
                container=container)
            messages.add_message(
                self.request,
                messages.WARNING,
                'The Inner Container {0} already exists, from Container '
                '{1} in {2}.'.format(
                    name,
                    container.name,
                    site_mappers.current_map_area))
        except InnerContainer.DoesNotExist:
            try:
                InnerContainer.objects.get(map_area=site_mappers.current_map_area,
                                           device_id=device_id)
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    'The Device {0} has already been allocated items in {1}, '
                    'select a diffrent device.'.format(
                        device_id,
                        site_mappers.current_map_area))
            except InnerContainer.DoesNotExist:
                InnerContainer.objects.create(
                    device_id=device_id,
                    boundry=boundry,
                    container=container,
                    name=name,
                    map_area=site_mappers.current_map_area,
                    labels=labels)
                inner_container_created = True
        return inner_container_created

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        context = self.get_context_data(**self.kwargs)
        context['form'] = form
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = self.request.GET.get('device_id')
        inner_container_name = self.request.GET.get('inner_container_name')
        boundry = self.request.GET.get('boundry')
        name = self.request.GET.get('container_name')
        labels = self.request.GET.get('labels', '')
        create_container_form = CreateContainerForm()
        if name:
            try:
                container = Container.objects.get(
                    name=name,
                    map_area=site_mappers.current_map_area)
            except Container.DoesNotExist:
                raise MapperError(
                    "Inner container can not exist without a container.")
        inner_container_created = False
        if inner_container_name and labels and boundry and device_id:
            inner_container_created = self.create_inner_container(
                labels,
                inner_container_name,
                device_id,
                boundry,
                container)
        if labels and inner_container_created:
            labels = labels.split(',')
        elif labels and not inner_container_created:
            labels = []
        context.update(
            map_area=site_mappers.current_map_area,
            labels=labels,
            create_container_form=create_container_form,
            inner_container_name=inner_container_name,
            container_name=name,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS,
            sectioning_statistics=self.sectioning_statistics)
        return context
