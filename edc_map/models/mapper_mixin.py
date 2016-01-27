from django.db import models

from ..exceptions import MapperError
from ..classes import site_mappers
from ..contants import CONFIRMED, UNCONFIRMED


class MapperMixin(models.Model):

    gps_confirm_latitude = models.DecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_confirm_longitude = models.DecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    target_radius = models.FloatField(
        default=.025,
        help_text='km',
        editable=False)

    distance_from_target = models.FloatField(
        null=True,
        editable=True,
        help_text='distance in meters')

    area_name = models.CharField(
        max_length=25,
        help_text='If the area name is incorrect, please contact the DMC immediately.',
        editable=False)

    action = models.CharField(
        max_length=25,
        null=True,
        default=UNCONFIRMED,
        editable=False)

    def save(self, *args, **kwargs):
        mapper = site_mappers.get_mapper(self.area_name)
        if self.gps_confirm_longitude and self.gps_confirm_latitude:
            mapper.location_in_map_area(self.gps_confirm_latitude, self.gps_confirm_longitude, MapperError)
            mapper.location_in_target(
                self.gps_confirm_latitude,
                self.gps_confirm_longitude,
                self.gps_target_lat,
                self.gps_target_lon,
                self.target_radius,
                MapperError,)
            self.distance_from_target = mapper.gps_distance_between_points(
                self.gps_confirm_latitude, self.gps_confirm_longitude, self.gps_target_lat, self.gps_target_lon) * 1000
        self.action = self.get_action()
        super(MapperMixin, self).save(*args, **kwargs)

    def get_action(self):
        retval = UNCONFIRMED
        if self.gps_confirm_latitude and self.gps_confirm_longitude:
            retval = CONFIRMED
        return retval

    class Meta:
        abstract = True
