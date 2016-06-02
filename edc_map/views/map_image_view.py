import os

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.apps import apps as django_apps

from ..snapshot import Snapshot


class MapImageView(TemplateView):

    template_name = 'edc_map/map_image.html'
    item_model = None  # model refered to by mapper / field value is passed in url
    item_model_field = None  # e.g. pk
    zoom_levels = ['16', '17', '18']
    app_label = 'edc_map'  # for django_apps AppsConfig registry, if not default

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MapImageView, self).dispatch(*args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super(MapImageView, self).get_context_data(**kwargs)
        obj = self.get_object()
        snapshot = Snapshot(
            obj.pk, latitude=obj.latitude, longitude=obj.longitude,
            map_area=self.kwargs.get('map_area'),
            zoom_levels=self.zoom_levels,
            app_label=self.app_label)
        context.update({
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'landmarks': snapshot.landmarks_by_label})
        context = dict(context, **self.get_image_filenames(snapshot.image_filenames))
        return context
