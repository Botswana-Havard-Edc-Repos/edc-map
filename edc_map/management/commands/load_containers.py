from django.apps import apps as django_apps
from django.core import serializers
from django.core.management.base import BaseCommand


def deserialize_json_file(file_name):
    try:
        json_txt = file_name.read()
        decoded = serializers.deserialize(
            "json", json_txt)
    except:
        return None
    return decoded


def upload_container(file_name, model_class):
    """Deserialise and upload model data from a json file.
    """
    with open(file_name) as infile:
        for container_obj in deserialize_json_file(infile):
            if container_obj.object._meta.get_fields():
                data = container_obj.object.__dict__
                del data['_state']
                model_class.objects.create(**data)


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
