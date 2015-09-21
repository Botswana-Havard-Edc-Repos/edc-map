from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from ..classes import Mapper, site_mappers
from ..exceptions import MapperError


def map_index(request, **kwargs):
    """Display filter options to chose what to display on the map

    Select the ward, section of the ward to use on the map
    """
    template = 'map_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    mapper_names = []
    mapper = None
    if not mapper_name:
        mapper_names = [mname for mname in site_mappers.get_registry()]
    else:
        mapper = site_mappers.get_registry(mapper_name)
    if mapper:
        if not issubclass(mapper, Mapper):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        mapper = site_mappers.get_registry(mapper_name)()
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'item_label': mapper.item_label,
                    'region_field_attr': mapper.region_field_attr,
                    'region_label': mapper.region_label,
                    'section_field_attr': mapper.section_field_attr,
                    'section_label': mapper.section_label,
                    'regions': mapper.regions,
                    'sections': mapper.sections,
                    'icons': mapper.icons,
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers
                },
                context_instance=RequestContext(request)
            )
    return render_to_response(
            template, {
                'mapper_names': mapper_names,
            },
            context_instance=RequestContext(request)
        )
