from django.apps import apps as django_apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Create items from a kmz google file with latitude and longitude.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='filepath')
        parser.add_argument('model', type=str, help='app_name.model')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE('Preparing load containers ...'))
        file_path = options['file_path']
        model = options['model']
        model_class = django_apps.get_model(model.split(','))
        upload_container(file_path, model_class)
        self.stdout.write(
            self.style.SUCCESS('Done.'))
