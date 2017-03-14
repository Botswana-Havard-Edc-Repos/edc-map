import os
from xml import sax
from zipfile import ZipFile

from django.conf import settings
from django.core.management.base import BaseCommand

from ...site_mappers import site_mappers
from ...placemark_handler import PlacemarkHandler
from ...exceptions import MapperError


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
    if f:
        file_extension = f.content_type.split("/")[1]
        filename = "{0}.{1}".format(community, file_extension)
        abs_filename = "{0}{1}".format(settings.MEDIA_ROOT, '/' + filename)
        if not os.path.exists(settings.MEDIA_ROOT):
            raise MapperError('The path does not exist. Got {0}'.format(abs_filename))
        with open(abs_filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    return filename


class Command(BaseCommand):

    help = 'Create items from a kmz google file with latitude and longitude.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='filepath')
        parser.add_argument('map_area', type=str, help='locatoin name')

    def handle(self, *args, **options):
        file_path = options['file_path']
        map_area = options['map_area']
        self.stdout.write(
            self.style.NOTICE('Preparing download items ...'))
        mapper = site_mappers.get_mapper(map_area)
        outstr = build_table(create_set_handler_parse_file(file_path).mapping)
        data_list = outstr.split('\n')
        data_list.pop(0)
        count = 0
        total_items = len(data_list)
        for item_gps_point in data_list:
            points = item_gps_point.split(',')
            if len(points) == 5:
                lat = float(points[2])
                lon = float(points[1])
                item = mapper.item_model(
                    **{'gps_target_lat': lat,
                       'gps_target_lon': lon,
                       'map_area': map_area})
                item.save()
                count += 1
                self.stdout.write(
                    self.style.NOTICE(
                        '{0} out of {1} items created ...'.format(
                            count, total_items)))
        self.stdout.write(
            self.style.SUCCESS('Done.'))
