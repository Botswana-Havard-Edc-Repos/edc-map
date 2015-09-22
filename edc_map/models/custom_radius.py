from django.db import models
from django.utils import timezone


class CustomRadius(models.Model):
    """A model completed by the user to allow a plot\'s GPS target radius to be changed.

    An instance is auto created once the criteria is met. See method plot.increase_plot_radius."""
    identifier = models.CharField(max_length=50, unique=True)

    radius = models.FloatField(
        default=25.0,
        help_text='meters')

    reason = models.CharField(max_length=25)

    created = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True
