from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import Mapper, site_mappers
from ..exceptions import MapperError


def kmz_file_upload(request, **kwargs):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'kmz_file_upload.html'
    mapper_name = kwargs.get('mapper_name', '')
    mapper = None
    if not mapper_name:
        mapper_names = [mname for mname in site_mappers.get_registry()]
    else:
        mapper = site_mappers.get_registry(mapper_name)
    if mapper:
        if not issubclass(mapper, Mapper):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        mapper = site_mappers.get_registry(mapper_name)()
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                },
                context_instance=RequestContext(request)
            )
