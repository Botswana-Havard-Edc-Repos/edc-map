import os
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def coordinates_to_gps(request, **kwargs):
    """Creates a .gpx file to store coordinates in the GPS receiver to guide to a location.

    fname: is an already existing file
    """
    template = 'sent.html'
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')

    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        if settings.DEVICE_ID == '99':
            raise MapperError('You are in the server, You can\'t dispatch the whole server data to a GPS receiver.')
        else:
            #TODO: if path does not exist fail gracefully
            if os.path.exists(settings.GPS_DEVICE):
                if os.path.exists(settings.GPS_FILE_NAME):
                    os.remove(settings.GPS_FILE_NAME)
                if not os.path.exists(settings.GPX_TEMPLATE):
                    raise MapperError('xml template file for GPS device does not exist, either run collectstatic or check if the file exists')    
                f = open(settings.GPX_TEMPLATE, 'r')
                line = f.readline()
                lines = f.read()
                f.close()
                wf = open(settings.GPS_FILE_NAME, 'a')
                wf.write(line)
                items = mapper.item_model.objects.all()
                for item in items:
                    identifier_name = str(getattr(item, mapper.identifier_field_attr))
                    lat = item.gps_target_lat
                    lon = item.gps_target_lon
                    ele = 0.0
                    city_village = mapper.map_area
                    str_from_edc = '<wpt lat="' + str(lat) + '" lon="' + str(lon) + '"><ele>' + str(ele) + '</ele>' + '<name>' + str(identifier_name) + '</name><extensions><gpxx:WaypointExtension><gpxx:Address><gpxx:City>' + str(city_village) + '</gpxx:City><gpxx:State>South Eastern</gpxx:State></gpxx:Address></gpxx:WaypointExtension></extensions>' + '</wpt>'
                    wf.write(str_from_edc)
                wf.write(lines)
                wf.close()
            else:
                template = 'dispatch_to_gps_index.html'
                message = 'Gps device not mounted'
                return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'message': message
                },
                context_instance=RequestContext(request)
            )
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'file_to_gps': settings.GPS_FILE_NAME
                },
                context_instance=RequestContext(request)
            )
