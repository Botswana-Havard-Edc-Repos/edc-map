import os
import shutil

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand
from edc_map.models import InnerContainer


class Command(BaseCommand):

    help = 'Create items from a kmz google file with latitude and longitude.'

    def add_arguments(self, parser):
        parser.add_argument('map_area', type=str, help='map_area')

    def handle(self, *args, **options):
        app_config = django_apps.get_app_config('edc_map')

        self.stdout.write(
            self.style.NOTICE('Preparing to load containers ...'))
        map_area = options['map_area']
        inner_containers = InnerContainer.objects.filter(map_area=map_area)
        for inner_container in inner_containers:
            item_identifiers = inner_container.identifier_labels
            total_items = len(item_identifiers)
            img_dir = os.path.join(
                app_config.image_folder, inner_container.device_id)
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            for item_identifier in item_identifiers:
                for zoom_level in app_config.zoom_levels:
                    file_name = item_identifier + zoom_level + '.jpg'
                    img_file = os.path.join(
                        app_config.image_folder, file_name)
                    if not os.path.exists(img_file):
                        self.stdout.write(
                            self.style.WARNING(f'Missing files {img_file}'))
                    if not os.path.exists(os.path.join(img_dir, file_name)):
                        shutil.copy2(img_file, img_dir)
            self.stdout.write(
                self.style.SUCCESS(
                    f'{total_items} Item images for {inner_container} moved to {img_dir}.'))
        self.stdout.write(
            self.style.SUCCESS('Done.'))
