from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_map.model_mixins import MapperDataModelMixin, LandmarkMixin


class ContainerManager(models.Manager):

    def get_by_natural_key(self, name, map_area):
        return self.get(name=name, map_area=map_area)


class InnerContainerManager(models.Manager):

    def get_by_natural_key(self, name, map_area, device_id, container_name, container_map_area):
        return self.get(
            name=name, map_area=map_area,
            device_id=device_id, container__name=container_name,
            container__map_area=container_map_area)


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

    objects = ContainerManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.name, self.map_area)

    def __str__(self):
        return '{0} {1}'.format(
            self.map_area,
            self.name,)

    @property
    def identifier_labels(self):
        """Returns identifier labels as a python list.
        """
        if self.labels:
            labels = self.labels.split(',')
            labels.pop(0)
            return labels
        return []

    @property
    def points(self):
        """Returns a list of polygon points."""
        points_list = []
        if self.boundry:
            points = self.boundry.split('|')
            del points[-1]
            for point in points:
                point = point.split(',')
                points_list.append(point)
            return points_list
        return points_list

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

    objects = InnerContainerManager()

    history = HistoricalRecords()

    def __str__(self):
        return '{0} {1} {2}, {3}'.format(
            self.device_id,
            self.container.name,
            self.name,
            self.map_area)

    def natural_key(self):
        return (self.name, self.map_area, self.device_id, self.container.natural_key())
    natural_key.dependencies = ['edc_map.container']

    @property
    def identifier_labels(self):
        """Returns identifier labels as a python list.
        """
        if self.labels:
            labels = self.labels.split(',')
            # clean up list
            labels = [x for x in labels if x]
            return labels
        return []

    @property
    def points(self):
        """Returns a list of polygon points."""
        points_list = []
        if self.boundry:
            points = self.boundry.split('|')
            del points[-1]
            for point in points:
                point = point.split(',')
                points_list.append(point)
            return points_list
        return points_list

    class Meta:
        app_label = 'edc_map'
        unique_together = ("device_id", "name", "map_area", "container")
