from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..classes import site_mappers


class MapImage(View):

    def __init__(self):
        self.context = {}
        self.template_name = 'map_image.html'

    def get(self, request, *args, **kwargs):
        obj_pk = kwargs.get('obj_pk', '')
        mapper_name = site_mappers.current_community
        mapper = site_mappers.get_mapper(mapper_name)
        map_zoom = kwargs.get('map_zoom', '1')
        if map_zoom == '1':
            file_name = obj_pk + '16'
        elif map_zoom == '2':
            file_name = obj_pk + '17'
        elif map_zoom == '3':
            file_name = obj_pk + '18'
        url = mapper.image_file_url(file_name)
        landmarks = mapper.landmarks
        landmarks_dict = mapper.close_landmarks(coordinates=[], landmarks=landmarks)
        self.context.update({
            'obj_pk': obj_pk,
            'url': url,
            'map_zoom_1': '1',
            'map_zoom_2': '2',
            'map_zoom_3': '3',
            'landmarks': landmarks_dict
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        self.context.update({
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):

        return super(MapImage, self).get_context_data(**kwargs)
