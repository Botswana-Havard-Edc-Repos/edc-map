from django.core.management.base import BaseCommand


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
