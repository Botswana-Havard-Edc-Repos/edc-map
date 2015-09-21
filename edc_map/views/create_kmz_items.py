import os
from xml import sax
from zipfile import ZipFile
# import xml.sax
# import xml.sax.handler
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError
from ..classes import PlacemarkHandler


def create_set_handler_parse_file(fname):
    """Create a Parser, set the Handler, and parse the file

        Unzip the KMZ and extract doc.kml, fname: is a .kmz file e.g'test.kmz'
    """
    kmz = ZipFile(fname, 'r')
    kml = kmz.open('doc.kml', 'r')

    parser = sax.make_parser()
    handler = PlacemarkHandler()
    parser.setContentHandler(handler)
    parser.parse(kml)
    kmz.close()
    return handler


def build_table(mapping):
    sep = ','

    output = 'Name' + sep + 'Coordinates\n'
    points = ''
    lines = ''
    shapes = ''
    for key in mapping:
        coord_str = mapping[key]['coordinates'] + sep

        if 'LookAt' in mapping[key]:  # points
            points += key + sep + coord_str + "\n"
        elif 'LineString' in mapping[key]:  # lines
            lines += key + sep + coord_str + "\n"
        else:  # shapes
            shapes += key + sep + coord_str + "\n"
    output += points + lines + shapes
    return output


def handle_uploaded_file(f, community):
    """Copies uploaded kmz file to settings.MEDIA_ROOT."""
    filename = None
    if file:
        file_extension = f.content_type.split("/")[1]
        filename = "{0}.{1}".format(community, file_extension)
        abs_filename = "{0}{1}".format(settings.MEDIA_ROOT, '/' + filename)
        if not os.path.exists(settings.MEDIA_ROOT):
            raise MapperError('The path does not exist. Got {0}'.format(abs_filename))
        with open(abs_filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    return filename,


def create_kmz_items(request, **kwargs):
    """Uploads item map saved on disk as an images e.g google map screenshot."""

    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        template = 'sucess_upload.html'

        if request.FILES['file']:
            filename = handle_uploaded_file(request.FILES['file'], mapper_name)
            file_path = str(settings.MEDIA_ROOT) + '/' + filename[0]
            outstr = build_table(create_set_handler_parse_file(file_path).mapping)
            data_list = outstr.split('\n')
            data_list.pop(0)
            count = 0
            for item_gps_point in data_list:
                points = item_gps_point.split(',')
                if len(points) == 5:
                    lat = float(points[2])
                    lon = float(points[1])
                    h = mapper.item_model(**{mapper.target_gps_lat_field_attr: lat, mapper.target_gps_lon_field_attr: lon, mapper.map_area_field_attr: mapper_name})
                    h.save()
                else:
                    pass
                count += 1
            message = 'The file ' + filename[0] + ' was uploaded successfully \n and {0} items where created'.format(count - 2)
        else:
            message = 'No file was uploaded'
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'message': message,
                },
                context_instance=RequestContext(request)
            )
