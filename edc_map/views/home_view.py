from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin

from ..models import InnerContainer, Container
from ..constants import SECTIONS, SUB_SECTIONS
from ..forms import ContainerSelectionForm
from ..exceptions import MapperError


class HomeView(EdcBaseViewMixin, TemplateView, FormView):

    form_class = ContainerSelectionForm
    app_config_name = 'edc_map'
    template_name = 'edc_map/home.html'

    def create_inner_container(
            self, labels, name, device_name, boundry, container):
        try:
            InnerContainer.objects.get(
                name=name)
        except InnerContainer.DoesNotExist:
            InnerContainer.objects.create(
                device_name=device_name,
                boundry=boundry,
                container=container,
                name=name,
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
        device_name = self.request.GET.get('device_name')
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
        if inner_container_name and labels and polygon_points and device_name:
            self.create_inner_container(
                labels,
                inner_container_name,
                device_name,
                polygon_points,
                container)
        context.update(
            map_area='test_community',
            labels=self.labels,
            inner_container_name=inner_container_name,
            container_name=name,
            container_names=SECTIONS,
            inner_container_names=SUB_SECTIONS)
        return context
