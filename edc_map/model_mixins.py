from django.db import models
from django.utils import timezone
from geopy import Point

from edc_map.exceptions import MapperError

from .site_mappers import site_mappers
from .validators import is_valid_map_area


class LandmarkMixin(models.Model):

    map_area = models.CharField(max_length=25)

    label = models.CharField(max_length=50)

    latitude = models.DecimalField(
        max_digits=20,
        null=True,
        decimal_places=15)

    longitude = models.DecimalField(
        max_digits=20,
        null=True,
        decimal_places=15)

    def __str__(self):
        return '{}: {}'.format(self.map_area, self.label)

    @property
    def point(self):
        return Point(self.latitude, self.longitude)

    @property
    def name(self):
        return self.label

    class Meta:
        abstract = True


class MapperDataModelMixin(models.Model):

    center_lat = models.DecimalField(
        max_digits=20,
        null=True,
        decimal_places=15)

    center_lon = models.DecimalField(
        max_digits=20,
        null=True,
        decimal_places=15)

    radius = models.DecimalField(
        max_digits=10,
        null=True,
        decimal_places=2)

    map_area = models.CharField(
        max_length=25)

    class Meta:
        abstract = True


class MapperModelMixin(models.Model):

    gps_confirmed_latitude = models.DecimalField(
        verbose_name='latitude',
        max_digits=20,
        null=True,
        blank=True,
        decimal_places=15)

    gps_confirmed_longitude = models.DecimalField(
        verbose_name='longitude',
        max_digits=20,
        null=True,
        blank=True,
        decimal_places=15)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=20,
        default=0.0,
        null=True,
        blank=True,
        decimal_places=15)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=20,
        default=0.0,
        null=True,
        blank=True,
        decimal_places=15)

    target_radius = models.FloatField(
        default=.025,
        null=True,
        blank=True,
        help_text='km')

    distance_from_target = models.FloatField(
        null=True,
        editable=False,
        help_text='distance in meters')

    map_area = models.CharField(
        max_length=25,
        validators=[is_valid_map_area])

    location_name = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    confirmed = models.BooleanField(
        default=False,
        editable=False,
        help_text="gps target is confirmed")

    section = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        verbose_name='Section')

    sub_section = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        verbose_name='Sub-section',
        help_text='')

    def save(self, *args, **kwargs):
        if self.gps_confirmed_longitude and self.gps_confirmed_latitude:
            self.confirmed = self.get_confirmed()
        else:
            self.distance_from_target = None
            self.confirmed = False
        super().save(*args, **kwargs)

    def common_clean(self):
        """Attempt to trigger MapperError exception if gps is not valid."""
        site_mappers.get_mapper(self.map_area)
        self.is_valid_target_or_raise()
        if self.gps_confirmed_longitude and self.gps_confirmed_latitude:
            self.get_confirmed()
        super().common_clean()

    @property
    def point(self):
        """Alias for confirmed_point."""
        return self.confirmed_point

    def is_valid_target_or_raise(self):
        mapper = site_mappers.get_mapper(self.map_area)
        try:
            mapper.raise_if_not_in_map_area(self.target_point)
        except MapperError as e:
            raise MapperError(
                'Invalid target GPS point. Got {}'.format(str(e)))

    @property
    def confirmed_point(self):
        """Returns a geopy point of the confirmed gps."""
        return Point(self.gps_confirmed_latitude, self.gps_confirmed_longitude)

    @property
    def target_point(self):
        """Returns a geopy point of the target gps."""
        return Point(self.gps_target_lat, self.gps_target_lon)

    def get_confirmed(self):
        """Returns True if plot is considered "confirmed" or raises an exception."""
        mapper = site_mappers.get_mapper(self.map_area)
        try:
            mapper.raise_if_not_in_map_area(self.confirmed_point)
        except MapperError as e:
            raise MapperError(
                'Invalid confirmation GPS point. Got {}'.format(str(e)))
        mapper.raise_if_not_in_radius(
            self.confirmed_point, self.target_point, self.target_radius,
            units='km', label='target location')
        self.distance_from_target = mapper.distance_between_points(
            self.confirmed_point, self.target_point, units='m')
        return True

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
