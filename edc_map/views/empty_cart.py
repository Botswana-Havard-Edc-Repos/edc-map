from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def empty_cart(request, message, **kwargs):
    """Empties cart.    """
    template = 'map_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        try:
            del request.session['identifiers']
            del request.session['icon']
        except KeyError:
            pass
        return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'regions': mapper.regions,
                'sections': mapper.sections,
                'icons': mapper.icons,
                'message': message,
                'item_label': mapper.item_model._meta.object_name,
                'region_label': mapper.region_label,
            },
            context_instance=RequestContext(request)
        )
