import os

from django.conf import settings
from ..classes import site_mappers
from ..exceptions import MapperError


class LocationToGps(object):

    def write_to_gps(self):
        """Write coordinates to GPS file."""

        mapper = site_mappers.get_mapper(site_mappers.current_community)
        line, lines = self.read_gps_template_file()
        wf = open(settings.GPS_FILE_NAME, 'a')
        wf.write(line)
        items = mapper.item_model.objects.all()
        for item in items:
            identifier = str(getattr(item, mapper.identifier_field_attr))
            lat = item.gps_target_lat
            lon = item.gps_target_lon
            ele = 0.0
            city_village = mapper.map_area
            str_from_edc = '<wpt lat="' + str(lat) + '" lon="' + str(lon) + '"><ele>' + str(ele) + '</ele>' + '<name>'
            str_from_edc += str(identifier) + '</name><extensions><gpxx:WaypointExtension><gpxx:Address><gpxx:City>'
            str_from_edc += str(city_village) + '</gpxx:City><gpxx:State>South Eastern</gpxx:State></gpxx:Address>'
            str_from_edc += '</gpxx:WaypointExtension></extensions></wpt>'
            wf.write(str_from_edc)
        wf.write(lines)
        wf.close()

    def read_gps_template_file(self):
        """Returns template xml structure of a gpx file, opening and closing strings."""

        line = None
        lines = None
        gps_file_directories = [settings.GPS_DEVICE, settings.GPX_TEMPLATE]
        if self.check_path_exists(gps_file_directories):
            if os.path.exists(settings.GPS_FILE_NAME):
                os.remove(settings.GPS_FILE_NAME)
            f = open(settings.GPX_TEMPLATE, 'r')
            line = f.readline()
            lines = f.read()
            f.close()
        if not (line and lines):
            raise MapperError('GPS template file might be empty at {0}.'.format(settings.GPX_TEMPLATE))
        return [line, lines]

    def check_path_exists(self, directories):
        """Return True if a list of files or directories exists."""
        exists = False
        for directory in directories:
            if os.path.exists(directory):
                exists = True
            else:
                raise MapperError('Make sure the file or director {0} exists.'.format(directory))
        return exists
