from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<coordinate>, e.g 24.1334456'
    help = 'calculate the degrees and minutes from degrees coordinate.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        # Ignore the negative on the cordinate for the latitude
        coordinate = float(args[0])
        degrees, minutes = divmod(coordinate * 60, 60)
        print "Degrees: {0}, minutes: {1}".format(degrees, minutes)
