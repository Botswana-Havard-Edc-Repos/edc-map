from django.db import models
from django.utils import timezone
from geopy import Point
# from django_crypto_fields.fields import EncryptedDecimalField

from .constants import CONFIRMED, UNCONFIRMED
from .site_mappers import site_mappers


class MapperModelMixin(models.Model):

    gps_confirm_latitude = models.DecimalField(
        verbose_name='latitude',
        max_digits=15,
        null=True,
        decimal_places=10)

    gps_confirm_longitude = models.DecimalField(
        verbose_name='longitude',
        max_digits=15,
        null=True,
        decimal_places=10)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=15,
        default=0.0,
        null=True,
        decimal_places=10)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=15,
        default=0.0,
        null=True,
        decimal_places=10)

    target_radius = models.FloatField(
        default=.025,
        help_text='km',
        editable=False)

    distance_from_target = models.FloatField(
        null=True,
        editable=True,
        help_text='distance in meters')

    map_area = models.CharField(
        max_length=25,
        help_text='If the area name is incorrect, please contact the DMC immediately.',
        editable=False)

    action = models.CharField(
        max_length=25,
        null=True,
        default=UNCONFIRMED,
        editable=False)

    section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Section',
        editable=False)

    sub_section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Sub-section',
        help_text=u'',
        editable=False)

    @property
    def point(self):
        return self.confirmed_point

    @property
    def confirmed_point(self):
        return Point(self.gps_confirm_latitude, self.gps_confirm_longitude)

    @property
    def target_point(self):
        return Point(self.gps_target_lat, self.gps_target_lon)

    def save(self, *args, **kwargs):
        if self.gps_confirm_longitude and self.gps_confirm_latitude:
            mapper = site_mappers.get_mapper(self.area_name)
            mapper.raise_if_not_in_map_area(self.confirmed_point)
            mapper.raise_if_not_in_radius(
                self.confirmed_point, self.target_point, self.target_radius,
                units='m', label='target location')
            self.distance_from_target = mapper.distance_between_points(
                self.confirmed_point, self.target_point, units='m')
        self.action = self.get_confirmation_status()
        super(MapperModelMixin, self).save(*args, **kwargs)

    def get_confirmation_status(self):
        retval = UNCONFIRMED
        if self.gps_confirm_latitude and self.gps_confirm_longitude:
            retval = CONFIRMED
        return retval

    class Meta:
        abstract = True


class CustomRadiusMixin(models.Model):
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
