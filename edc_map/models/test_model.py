from django.db import models

from ..models import MapperMixin


class TestModel(MapperMixin):

    location_identifier = models.CharField(
        verbose_name="Location Identifier",
        max_length=50)

    class Meta:
        app_label = 'edc_map'
