from django.db import models


class Plot(models.Model):

    plot_identifier = models.CharField(
        verbose_name='Plot Identifier',
        max_length=25,
        unique=True,
    )

    gps_degrees_s = models.DecimalField(
        verbose_name='GPS Degrees-South',
        max_digits=10,
        null=True,
        decimal_places=0)

    gps_minutes_s = models.DecimalField(
        verbose_name='GPS Minutes-South',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_degrees_e = models.DecimalField(
        verbose_name='GPS Degrees-East',
        null=True,
        max_digits=10,
        decimal_places=0)

    gps_minutes_e = models.DecimalField(
        verbose_name='GPS Minutes-East',
        max_digits=10,
        null=True,
        decimal_places=4)

    gps_lon = models.DecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_lat = models.DecimalField(
        verbose_name='latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lon = models.DecimalField(
        verbose_name='target waypoint longitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    gps_target_lat = models.DecimalField(
        verbose_name='target waypoint latitude',
        max_digits=10,
        null=True,
        decimal_places=6)

    target_radius = models.FloatField(
        default=.025,
        help_text='km',
    )

    distance_from_target = models.FloatField(
        null=True,
        editable=True,
        help_text='distance in meters')

    # Google map static images for this plots with different zoom levels.
    # uploaded_map_16, uploaded_map_17, uploaded_map_18 zoom level 16, 17, 18 respectively
    uploaded_map_16 = models.CharField(
        verbose_name="Map image at zoom level 16",
        max_length=25,
        null=True,
        blank=True,
    )

    uploaded_map_17 = models.CharField(
        verbose_name="Map image at zoom level 17",
        max_length=25,
        null=True,
        blank=True,
    )

    uploaded_map_18 = models.CharField(
        verbose_name="Map image at zoom level 18",
        max_length=25,
        null=True,
        blank=True,
    )

    community = models.CharField(
        max_length=25,
    )

    section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Section',
    )

    sub_section = models.CharField(
        max_length=25,
        null=True,
        verbose_name='Sub-section',
        help_text=u'',
    )

    class Meta:
        app_label = 'edc_map'
