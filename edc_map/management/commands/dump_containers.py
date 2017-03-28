from django.core import serializers
from django.core.management.base import BaseCommand

from ...models import Container, InnerContainer


def dump_container_data_to_json(file_names, map_area):
    """Dump containers to json.
    """
    container_type = [Container, InnerContainer]

    for obj, obj_file in zip(container_type, file_names):
        with open(obj_file, 'a') as outfile:
            container_objects = obj.objects.filter(map_area=map_area)
            json_txt = serializers.serialize(
                "json", container_objects)
            outfile.write(json_txt)


class Command(BaseCommand):

    help = 'Create items from a kmz google file with latitude and longitude.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='filepath')
        parser.add_argument('map_area', type=str, help='locatoin name')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE('Preparing dump containers ...'))
        file_path = options['file_path']
        map_area = options['map_area']
        container_filename = file_path + map_area + 'container.json'
        inner_container_filename = file_path + map_area + 'inner_container.json'
        files = [container_filename, inner_container_filename]
        dump_container_data_to_json(files)
        self.stdout.write(
            self.style.SUCCESS('Done.'))
