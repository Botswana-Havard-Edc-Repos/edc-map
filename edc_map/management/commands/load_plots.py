import os
import fnmatch
from xml import sax
from zipfile import ZipFile
# import xml.sax
# import xml.sax.handler

from django.core.management.base import BaseCommand, CommandError

from ...classes import site_mappers
from ...exceptions import MapperError
from ...classes import PlacemarkHandler


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


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community_name e.g otse>, <file_path e.g /home/django/>'
    help = 'Creates plots in the database from a kmz file.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Missing \'using\' parameters.')

        mapper_name = args[0]
        file_path = str(args[1])
        site_mappers.autodiscover()
        if not site_mappers.get_registry(mapper_name):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        else:
            mapper = site_mappers.get_registry(mapper_name)()
            filename = None
            for file in os.listdir(str(args[1]) + '/'):
                if fnmatch.fnmatch(file, str(mapper_name.title()) + '*kmz'):
                    filename = os.path.join(file_path, file)
            if not os.path.exists(filename):
                raise IOError("Files do not exist in the path: {0}.".format(filename))
            outstr = build_table(create_set_handler_parse_file(filename).mapping)
            data_list = outstr.split('\n')
            data_list.pop(0)
            count = 0
            for item_gps_point in data_list:
                points = item_gps_point.split(',')
                if len(points) == 5:
                    lat = float(points[2])
                    lon = float(points[1])
                    h = mapper.get_item_model_cls()(**{mapper.target_gps_lat_field_attr: lat, mapper.target_gps_lon_field_attr: lon, mapper.map_area_field_attr: mapper_name})
                    h.save()
                else:
                    pass
                print "Total number of plots added {0} out of {1}.".format(count, len(data_list) - 1)
                count += 1
            message = 'The file ' + filename[0] + ' was uploaded successfully \n and {0} items where created'.format(count - 2)
            print message, '\n', "Sucess!!"
