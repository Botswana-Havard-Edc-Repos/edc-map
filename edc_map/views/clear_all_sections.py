from django.shortcuts import render_to_response
from django.template import RequestContext
from ..exceptions import MapperError
from ..classes import site_mappers


def clear_all_sections(request, **kwargs):
    """Clears all sections for a given region."""

    template = 'clear_all_sections.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'item_label': mapper.item_label,
                    'section_label': mapper.section_label,
                    'region_label': '{0}s'.format(mapper.region_label),
                    'regions': mapper.regions,
                    'region_field_attr': mapper.region_field_attr,
                 },
                context_instance=RequestContext(request)
            )
