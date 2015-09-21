from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def get_polygon_array(request, **kwargs):
    """Adds a list of identifiers to a shopping cart and returns back to map or checkout cart.

    The list of identifiers of points that are within a polygon.
    """
    template = 'get_polygon_array.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        polygon_array = request.GET.get('polygon')
        if polygon_array:
            polygon_array = polygon_array.split("),(")
            polygon_array[0] = polygon_array[0][1:]
            polygon_array[-1] = polygon_array[0]

            point_tuple = ()
            for pnts in polygon_array:
                point_tuple = point_tuple + (pnts,)

        return render_to_response(
            template, {
                'mapper_name': mapper_name,
                'point_tuple': point_tuple,
                'map_area': mapper.map_area
            },
            context_instance=RequestContext(request)
        )
