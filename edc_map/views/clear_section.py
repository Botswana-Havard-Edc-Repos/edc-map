from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def clear_section(request, **kwargs):
    """Assigns selected section to None for all items in a region.

    Filters the items by ward and assigns the ward_section field to Null for the whole ward
    This allows for re-assigning of ward section for items within a ward.
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        selected_region = request.POST.get(mapper.region_field_attr)
        items = mapper.item_model.objects.filter(**{mapper.region_field_attr: selected_region})
        if items:
            for item in items:
                setattr(item, mapper.region_field_attr, None)
                setattr(item, mapper.section_field_attr, None)
                item.save()
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                'map_section.html', {
                    'mapper_name': mapper_name,
                    'regions': mapper.regions,
                    'region_label': mapper.region_label,
                    'icons': mapper.icons,
                    'sections': mapper.sections,
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers,
                    'show_map': 0,
                    'has_items': True,
                },
                context_instance=RequestContext(request)
            )
