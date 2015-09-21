import os
from urllib import urlretrieve
from time import sleep
from operator import itemgetter

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.conf import settings

from ...classes import site_mappers
from ...exceptions import MapperError



class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community>'
    help = 'Creates map images for all the items.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')

        mapper_name = args[0]
        site_mappers.autodiscover()
        if not site_mappers.get_registry(mapper_name):
            raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
        else:
            mapper = site_mappers.get_registry(mapper_name)()
            letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                    "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            items = mapper.item_model.objects.filter(Q(**{mapper.map_area_field_attr: mapper_name, mapper.item_selected_field: 2}) | Q(**{mapper.map_area_field_attr: mapper_name, mapper.item_selected_field: 1}))
            landmarks = mapper.landmarks
            url_str = ''
            file_name_18 = ''
            file_name_17 = ''
            file_name_16 = ''
            folder = settings.MEDIA_ROOT
            print "folder directions", folder
            count = 0
            for item in items:
                zoom_level = 0
                zoom = 18
                while zoom_level < 3:
                    url_str = 'http://maps.google.com/maps/api/staticmap?size=640x600&maptype=satellite&scale:2&format=png32&zoom=' + str(zoom) + '&center='
                    url_str += str(getattr(item, mapper.target_gps_lat_field_attr)) + ',' + str(getattr(item, mapper.target_gps_lon_field_attr)) + '&'
                    lmarks = []
                    for mark in landmarks:
                        lat = getattr(item, mapper.target_gps_lat_field_attr)
                        lon = getattr(item, mapper.target_gps_lon_field_attr)
                        dist = mapper.gps_distance_between_points(lat, lon, mark[1], mark[2])
                        lmarks.append([dist, landmarks[0], mark[1], mark[2]])
                    lmark = sorted(lmarks, key=itemgetter(0))
                    markers_l = mapper.make_dictionary(letters, lmark)
                    markers_str = ''
                    for key, value in markers_l.iteritems():
                        if key:
                            markers_str += 'markers=color:blue%7Clabel:' + key + '%7C' + str(value[2]) + ',' + str(value[3]) + '&'
                    url_str += markers_str
                    url_str += 'markers=color:red%7C' + str(getattr(item, mapper.target_gps_lat_field_attr)) + ',' + str(getattr(item, mapper.target_gps_lon_field_attr)) + "&key=AIzaSyC-N1j8zQ0g8ElLraVfOGcxaBUd2vBne2o" + '&sensor=false'
                    name = getattr(item, mapper.identifier_field_attr)
                    if zoom == 18:
                        file_name_18 = folder + '/' + name + '_18.jpg'
                        if not os.path.exists(file_name_18):
                            urlretrieve(url_str, file_name_18)
                            sleep(2)
                    elif zoom == 17:
                        file_name_17 = folder + '/' + name + '_17.jpg'
                        if not os.path.exists(file_name_17):
                            urlretrieve(url_str, file_name_17)
                            sleep(2)
                    else:
                        file_name_16 = folder + '/' + name + '.jpg'
                        if not os.path.exists(file_name_16):
                            urlretrieve(url_str, file_name_16)
                            sleep(2)
                    print "The image at zoom level: " + str(zoom) + " of plot: " + str(name) + " is done"
                    zoom -= 1
                    zoom_level += 1
                    item.uploaded_map_18 = name + '_18.jpg'
                    item.uploaded_map_17 = name + '_17.jpg'
                    item.uploaded_map_16 = name + '.jpg'
                    item.save()
                count += 1
                print str((count / float(len(items))) * 100) + ' percent done! only ' + str(len(items) - count) + ' more pictures to download'
