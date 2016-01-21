from django.db import models

from .custom_radius import CustomRadius


class MapperMixin(models.Model):

    CUSTOM_RADIUS_MODEL = CustomRadius
    CUSTOM_RADIUS_REASONS = ['dogs', 'locked_gate']

    gps_lon = models.DecimalField(
        verbose_name='longitude',
        max_digits=10,
        null=True,
        decimal_places=3)

    gps_lat = models.DecimalField(
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

#     def save(self, *args, **kwargs):
#         # unless overridden, if self.community != to mapper.map_area, raises
#         self.verify_plot_community_with_current_mapper(self.community)
#         # if self.community does not get valid mapper, will raise an error that should be caught in forms.py
#         mapper_cls = site_mappers.registry.get(self.community)
#         mapper = mapper_cls()
#         # if user added/updated gps_degrees_[es] and gps_minutes_[es], update gps_lat, gps_lon
#         if (self.gps_degrees_e and self.gps_degrees_s and self.gps_minutes_e and self.gps_minutes_s):
#             self.gps_lat = mapper.get_gps_lat(self.gps_degrees_s, self.gps_minutes_s)
#             self.gps_lon = mapper.get_gps_lon(self.gps_degrees_e, self.gps_minutes_e)
#             mapper.verify_gps_location(self.gps_lat, self.gps_lon, MapperError)
#             mapper.verify_gps_to_target(self.gps_lat, self.gps_lon, self.gps_target_lat,
#                                         self.gps_target_lon, self.target_radius, MapperError,
#                                         custom_radius=self.custom_radius)
#             self.distance_from_target = mapper.gps_distance_between_points(
#                 self.gps_lat, self.gps_lon, self.gps_target_lat, self.gps_target_lon) * 1000
#         try:
#             update_fields = kwargs.get('update_fields')
#             update_fields.append(['distance_from_target', 'plot_identifier', 'user_modified'])
#             kwargs.update({'update_fields': list(set(update_fields))})
#         except AttributeError:
#             pass
#         super(MapperMixin, self).save(*args, **kwargs)

#     def gps(self):
#         return "S{0} {1} E{2} {3}".format(self.gps_degrees_s, self.gps_minutes_s,
#                                           self.gps_degrees_e, self.gps_minutes_e)

#     @property
#     def target_radius_in_meters(self):
#         return self.target_radius * 1000
# 
#     @property
#     def custom_radius(self):
#         CustomRadius = self.CUSTOM_RADIUS_MODEL
#         try:
#             return CustomRadius.objects.get(plot=self)
#         except CustomRadius.DoesNotExist:
#             return None

#     @property
#     def increase_plot_radius(self):
#         """Returns an instance of IncreasePlotRadius if the user should be
#         allowed to change the target_radius otherwise returns None.
# 
#         Plot must be inaccessible and the last reason (of 3) be either "dogs"
#         or "locked gate" """
#         PlotLogEntry = self.PLOT_LOG_MODEL
#         IncreasePlotRadius = self.INCREASE_RADIUS_MODEL
#         created = False
#         increase_plot_radius = None
#         try:
#             increase_plot_radius = IncreasePlotRadius.objects.get(plot=self)
#         except IncreasePlotRadius.DoesNotExist:
#             if self.plot_inaccessible:
#                 plot_log_entries = PlotLogEntry.objects.filter(
#                     plot_log__plot__id=self.id).order_by('report_datetime')
#                 if plot_log_entries[2].reason in self.CUSTOM_RADIUS_REASONS:
#                     increase_plot_radius = IncreasePlotRadius.objects.create(plot=self)
#                     created = True
#         except IndexError:
#             pass
#         return increase_plot_radius, created
# 
#     def verify_plot_community_with_current_mapper(self, community, exception_cls=None):
#         """Returns True if the plot.community = the current mapper.map_area.
# 
#         This check can be disabled using the settings attribute VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER.
#         """
#         exception_cls = exception_cls or ValidationError
#         try:
#             verify_plot_community_with_current_mapper = settings.VERIFY_PLOT_COMMUNITY_WITH_CURRENT_MAPPER
#         except AttributeError:
#             verify_plot_community_with_current_mapper = True
#         if verify_plot_community_with_current_mapper:
#             if community != site_mappers.get_current_mapper().map_area:
#                 raise exception_cls(
#                     'Plot community does not correspond with the current mapper '
#                     'community of \'{}\'. Got \'{}\'.'.format(
#                         site_mappers.get_current_mapper().map_area, community))

    class Meta:
        app_label = 'edc_map'
