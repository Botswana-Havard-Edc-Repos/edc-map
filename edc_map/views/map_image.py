from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers


class MapImage(View):

    def __init__(self):
        self.context = {}
        self.template_name = 'map_image_include.html'
        self.mapper = site_mappers.get_mapper('test_area')

    def get(self, request, *args, **kwargs):
        obj_pk = 'wer23rf23r2rf5h56h5nbs5'
        url = self.mapper.image_file_url(obj_pk)
        landmarks = self.mapper.close_landmarks(coordinates=[], landmarks=[])
        self.context.update({
            'obj_pk': obj_pk,
            'url': url,
            'landmarks': landmarks
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        obj_pk = 'wer23rf23r2rf5h56h5nbs5'
        self.context.update({
            'obj_pk': obj_pk
        })
        return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))

    def get_context_data(self, **kwargs):

        return super(MapImage, self).get_context_data(**kwargs)
