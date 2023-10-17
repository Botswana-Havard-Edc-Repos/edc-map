import os

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError

from edc_map.fetch_images import FetchImages
from edc_map.snapshot import Snapshot
from ...site_mappers import site_mappers
from ...models import InnerContainer


class Command(BaseCommand):

    help = 'Fetch map images from google given a model listing the gps coordinates.'

    @property
    def identifier_field_attr(self):
        app_config = django_apps.get_app_config('edc_map')
        return app_config.identifier_field_attr

    @property
    def item_identifiers(self):
        edc_device_app_config = django_apps.get_app_config('edc_device')
        device_id = edc_device_app_config.device_id
        try:
            inner_containers = InnerContainer.objects.get(
                map_area=site_mappers.current_map_area, device_id=device_id)
            return inner_containers.identifier_labels
        except InnerContainer.DoesNotExist:
            return []
        return []

    def add_arguments(self, parser):
        # parser.add_argument('app_config',
        # type=str, help='app config for edc_map or other map app')
        parser.add_argument('model', type=str, help='app_label.model_name')
        parser.add_argument('max_downloads', type=int,
                            help='Maximum number of concurrent downloads')

    def handle(self, *args, **options):
        download_items = []
        app_config = django_apps.get_app_config('edc_map')
        try:
            model = django_apps.get_model(*options['model'].split('.'))
        except LookupError as e:
            raise CommandError(str(e))
        sephamores_count = options['max_downloads']
        qs = model.objects.filter(**{
            'map_area': site_mappers.current_map_area,
            '{0}__in'.format(self.identifier_field_attr): self.item_identifiers})
        record_count = qs.count()
        self.stdout.write(
            self.style.NOTICE('Preparing download items ...'))
        self.stdout.write(
            self.style.NOTICE('  * found {} records.'.format(record_count)))
        for obj in qs:
            s = Snapshot(obj.plot_identifier, obj.target_point, obj.map_area,
                         zoom_levels=app_config.zoom_levels)
            for zoom_level in app_config.zoom_levels:
                if not os.path.exists(s.image_filename(zoom_level, include_path=True)):
                    download_items.append(
                        (s.image_url(zoom_level), s.image_filename(zoom_level, include_path=True)))
        if len(download_items) > 0:
            self.stdout.write(
                self.style.NOTICE('  * fetching {} download items.'.format(len(download_items))))
            fetch_images = FetchImages(download_items=download_items, sephamores=sephamores_count)
            fetch_images.fetch()
        else:
            self.stdout.write(
                self.style.NOTICE('  * {}/{} images already exist.'.format(
                    record_count - len(download_items), record_count)))
        self.stdout.write(
            self.style.SUCCESS('Done.'))
