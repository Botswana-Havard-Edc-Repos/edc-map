from django.views.generic.base import TemplateView

from ..site_mappers import site_mappers
from ..snapshot import Snapshot


class MapImage(TemplateView):

    template_name = 'edc_map/map_image.html'

    def get_context_data(self, **kwargs):
        context = super(MapImage, self).get_context_data(kwargs)
        mapper_name = site_mappers.current_community
        mapper = site_mappers.get_mapper(mapper_name)
        snapshot = Snapshot()
        obj_pk = self.kwargs.get('obj_pk', '')
        map_zoom = kwargs.get('map_zoom', '1')
        if map_zoom == '1':
            file_name = obj_pk + '16'
        elif map_zoom == '2':
            file_name = obj_pk + '17'
        elif map_zoom == '3':
            file_name = obj_pk + '18'
        url = snapshot.image_file_url(file_name)
        landmarks = mapper.landmarks
        landmarks_dict = snapshot.close_landmarks(coordinates=[], landmarks=landmarks)
        context.update({
            'obj_pk': obj_pk,
            'url': url,
            'map_zoom_1': '1',
            'map_zoom_2': '2',
            'map_zoom_3': '3',
            'landmarks': landmarks_dict
        })
        return context

#     def post(self, request, *args, **kwargs):
#         self.context.update({
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
