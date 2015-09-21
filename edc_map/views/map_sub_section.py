from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def map_sub_sections(request, **kwargs):
    """Select ward and section to separate items into section in a ward

    The selected ward and section are going to be use to set a section for the ward selected.

   """
    template = 'map_sub_section.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
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
                'regions': mapper.regions,
                'sections': mapper.sections,
                'icons': mapper.icons,
                'item_region_field': mapper.region_field_attr,
                'region_label': mapper.region_label,
                'section_label': mapper.section_label,
                'session_icon': icon,
                'cart_size': cart_size,
                'identifiers': identifiers,
                'section_field_attr': mapper.section_field_attr,
                'show_map': 1,
                'has_items': True,
                'option': 'plot'
            },
            context_instance=RequestContext(request))
