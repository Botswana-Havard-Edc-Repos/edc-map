from django.db import models
import ast

from edc_base.model.models import BaseUuidModel
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


class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Container(BaseUuidModel):

    labels = ListField(null=True)

    container_name = models.CharField(
        max_length=10,
        null=True)

    map_area = models.CharField(
        max_length=25,
        null=True)

    container_boundry = ListField(null=True)

    def __str__(self):
        return '{0} {1}'.format(
            self.map_area,
            self.container_name,)

    @property
    def identifier_labels(self):
        """Returns a list of item labels."""
        if self.labels:
            return ast.literal_eval(self.labels)
        return None

    @property
    def container_points(self):
        """Returns a list of polygon points."""
        if self.container_boundry:
            return ast.literal_eval(self.container_boundry)
        return None

    class Meta:
        app_label = 'edc_map'
        unique_together = ("container_name", "map_area")


class InnerContainer(BaseUuidModel):

    labels = ListField(null=True)

    container = models.ForeignKey(Container, null=True)

    username = models.CharField(
        verbose_name='Username',
        max_length=25,
        unique=True,
        null=True,)

    inner_container_name = models.CharField(
        max_length=10,
        null=True)

    inner_container_boundry = ListField(null=True)

    def __str__(self):
        return '{0} {1} {2}'.format(
            self.username,
            self.container.container_name,
            self.inner_container_name)

    @property
    def identifier_labels(self):
        """Returns a list of item labels."""
        if self.labels:
            return ast.literal_eval(self.labels)
        return None

    @property
    def inner_container_points(self):
        """Returns a list of polygon points."""
        if self.inner_container_boundry:
            return ast.literal_eval(self.inner_container_boundry)
        return None

    class Meta:
        app_label = 'edc_map'
        unique_together = ("username", "inner_container_name")
