from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError
from ..utils import calc_dist, get_longitude, get_latitude


def db_update(request, **kwargs):
    """Updates coordinates of an entered item identifier

         Filter items by entered item then save the new coordinates of that item
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        template = "db_update.html"
        identifier = request.POST.get('identifier')
        gps_s = request.POST.get('gps_s')
        longitude = request.POST.get('lon')
        gps_e = request.POST.get('gps_e')
        latitude = request.POST.get('lat')
        items = mapper.item_model.objects.filter(**{mapper.identifier_field_attr: identifier})
        lon = get_longitude(gps_s, longitude)
        lat = get_latitude(gps_e, latitude)
        for item in items:
            setattr(item, mapper.gps_e_field_attr, gps_e)
            setattr(item, mapper.gps_latitude_field_attr, latitude)
            setattr(item, mapper.gps_s_field_attr, gps_s)
            setattr(item, mapper.gps_longitude_field_attr, longitude)
            distance = calc_dist(lat, lon, mapper.gps_center_lat, mapper.gps_center_lon)
            if distance <= mapper.gps_radius:
                item.save()
            else:
                return HttpResponse("The coordinates you entered are outside {0}, check if you have made errors.".format(mapper.map_area))
        return render_to_response(
                    template,
                context_instance=RequestContext(request)
            )
