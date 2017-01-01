import json
import os

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from ..snapshot import Snapshot


class MapImageView(TemplateView):

    template_name = 'edc_map/map_image_view.html'
    item_model = None  # model refered to by mapper / field value is passed in url
    item_model_field = None  # e.g. pk
    filename_field = 'pk'  # maybe you rather use subject_identifier, if available
    zoom_levels = ['16', '17', '18']
    app_label = 'edc_map'  # for django_apps AppsConfig registry, if not default
    map_image_view_base_html = 'edc_base/base.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        """Return an instance of the item model."""
        value = self.kwargs.get(self.item_model_field)
        try:
            obj = self.item_model.objects.get(**{self.item_model_field: value})
        except self.item_model.DoesNotExist:
            obj = None
        return obj

    @property
    def image_folder_url(self):
        app = django_apps.get_app_config(self.app_label)
        return app.image_folder_url

    def get_image_filenames(self, filenames):
        """Return a dictionary of filenames for the three zoom levels."""
        return {
            'image_file_zoom_level_one': os.path.join(self.image_folder_url, filenames.get('16')),
            'image_file_zoom_level_two': os.path.join(self.image_folder_url, filenames.get('17')),
            'image_file_zoom_level_three': os.path.join(self.image_folder_url, filenames.get('18'))}

    def get_image_filenames2(self, filenames):
        """Return a dictionary of filenames for the three zoom levels."""
        image_filenames = {}
        for zoom_level in self.zoom_levels:
            image_filenames.update({
                zoom_level: os.path.join(self.image_folder_url, filenames.get(zoom_level))})
        return image_filenames

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        if obj:
            snapshot = Snapshot(
                getattr(obj, self.filename_field), point=obj.point,
                map_area=self.kwargs.get('map_area'),
                zoom_levels=self.zoom_levels)
            context.update({
                'point': obj.point,
                'landmarks': snapshot.landmarks_by_label,
                'image_filenames': self.get_image_filenames2(snapshot.image_filenames)})
            context = dict(context, **self.get_image_filenames(snapshot.image_filenames))
        else:
            context.update({
                'point': None,
                'landmarks': None,
                'image_filenames': None})
        json_data = json.dumps(
            dict(zoom_levels=self.zoom_levels, image_filenames=context['image_filenames']),
            cls=DjangoJSONEncoder)
        context.update(
            zoom_levels=self.zoom_levels,
            json_data=json_data,
            item_label=context.get('item_label', 'Subject'),
            map_image_view_base_html=self.map_image_view_base_html)
        return context
