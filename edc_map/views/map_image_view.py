from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from ..snapshot import Snapshot


class MapImageView(TemplateView):

    template_name = 'edc_map/map_image.html'
    item_model = None  # model refered to by mapper / field value is passed in url
    item_model_field = None  # e.g. pk
    zoom_levels = ['16', '17', '18']

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

    def get_image_filenames(self, filenames):
        """Return a dictionary of filenames for the three zoom levels."""
        return {
            'image_file_zoom_level_one': filenames.get('16'),
            'image_file_zoom_level_two': filenames.get('17'),
            'image_file_zoom_level_three': filenames.get('18')}

    def get_context_data(self, **kwargs):
        context = super(MapImageView, self).get_context_data(**kwargs)
        obj = self.get_object()
        snapshot = Snapshot(
            obj.pk, latitude=obj.latitude, longitude=obj.longitude,
            map_area=self.kwargs.get('map_area'),
            zoom_levels=self.zoom_levels)
        context.update({
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'landmarks': snapshot.nearby_landmarks})
        context = dict(context, **self.get_image_filenames(snapshot.image_filenames))
        return context

#     def get_context_data(self, **kwargs):
#         context = super(MapImageView, self).get_context_data(kwargs)
#         mapper_name = site_mappers.current_community
#         mapper = site_mappers.get_mapper(mapper_name)
#         snapshot = Snapshot()
#         obj_pk = self.kwargs.get('pk', '')
#         zoom_level = self.kwargs.get('zoom_level', '1')
#         image_files = {
#             '1': obj_pk + '16',
#             '2': obj_pk + '17',
#             '3': obj_pk + '18'}
#         selected_image_file = image_files.get(zoom_level)
#         url = snapshot.image_file_url(selected_image_file)
#         landmarks_dict = snapshot.close_landmarks(coordinates=[], landmarks=mapper.landmarks)
#         context.update({
#             'obj_pk': obj_pk,
#             'url': url,
#             'zoom_level_1': '1',
#             'zoom_level_2': '2',
#             'zoom_level_3': '3',
#             'landmarks': landmarks_dict,
#             'image_files': image_files,
#         })
#         return context
