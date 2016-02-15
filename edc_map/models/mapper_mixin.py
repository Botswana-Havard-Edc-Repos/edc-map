from django.db import models

from ..exceptions import MapperError
from ..classes import site_mappers
from ..contants import CONFIRMED, UNCONFIRMED
from edc_base.encrypted_fields import EncryptedDecimalField
from edc_map.classes.snapshot import Snapshot


class MapperMixin(models.Model):

    gps_confirm_latitude = EncryptedDecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_confirm_longitude = EncryptedDecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_target_lon = EncryptedDecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        default=0.0,
        null=True,
        decimal_places=3)

    gps_target_lat = EncryptedDecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        default=0.0,
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

    def store_image(self):
        """Generate images with 3 zoom levels, 16, 17, 18."""

        mapper = site_mappers.get_mapper(self.area_name)
        landmarks = mapper.landmarks
        snapshot = Snapshot()
        coordinates = [self.gps_target_lat, self.gps_target_lon]
        zoom_level = 16
        while zoom_level < 19:
            url = snapshot.google_image_url(coordinates, landmarks, zoom_level)
            image_name = str(self.pk) + str(zoom_level)
            snapshot.grep_image(url, image_name)
            zoom_level += 1

    class Meta:
        abstract = True
