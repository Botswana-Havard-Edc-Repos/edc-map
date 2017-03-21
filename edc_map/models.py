import ast

from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model_mixins import BaseUuidModel
from edc_map.model_mixins import MapperDataModelMixin, LandmarkMixin


class Landmark(LandmarkMixin, BaseUuidModel):

    class Meta:
        app_label = 'edc_map'


class MapperData(MapperDataModelMixin, BaseUuidModel):

    map_code = models.CharField(
        max_length=10)

    pair = models.IntegerField()

    intervention = models.BooleanField(default=False)

    class Meta:
        app_label = 'edc_map'


class Container(BaseUuidModel):

    labels = models.TextField(null=True)

    name = models.CharField(
        max_length=10,
        null=True)

    map_area = models.CharField(
        max_length=25,
        null=True)

    boundry = models.TextField(null=True)

    def __str__(self):
        return '{0} {1}'.format(
            self.map_area,
            self.name,)

    @property
    def identifier_labels(self):
        """Returns a list of item labels."""
        if self.labels:
            return ast.literal_eval(self.labels)
        return None

    @property
    def points(self):
        """Returns a list of polygon points."""
        if self.boundry:
            return ast.literal_eval(self.boundry)
        return None

    class Meta:
        app_label = 'edc_map'
        unique_together = ("name", "map_area")


class InnerContainer(BaseUuidModel):

    labels = models.TextField(null=True)

    container = models.ForeignKey(Container, on_delete=PROTECT)

    device_id = models.CharField(
        verbose_name='Device Id',
        max_length=25,
        null=True,)

    map_area = models.CharField(
        max_length=25,
        null=True)

    name = models.CharField(
        max_length=10,
        null=True)

    boundry = models.TextField(null=True)

    def __str__(self):
        return '{0} {1} {2}, {3}'.format(
            self.device_id,
            self.container.name,
            self.name,
            self.map_area)

    @property
    def identifier_labels(self):
        """Returns a list of item labels."""
        if self.labels:
            return ast.literal_eval(self.labels)
        return None

    @property
    def points(self):
        """Returns a list of polygon points."""
        if self.boundry:
            return ast.literal_eval(self.boundry)
        return None

    class Meta:
        app_label = 'edc_map'
        unique_together = ("device_id", "name", "map_area")
