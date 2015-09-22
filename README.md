
# edc-map

classes to link data collection to GPS points and boundaries


Add to settings:

	VERIFY_GPS = True
	CURRENT_COMMUNITY = 'test_community'
	
Like this:

	from edc_map.models import MapperMixin
	
	class Plot(MapperMixin):
	
		plot_identifier = models.CharField(max_length=25)

		class Meta:
			app_label = 'my_app'
			
To allow a user to change the plot radius, a log model is used:

	from edc_map.models import RadiusLog
	
	class MyRadiusLog(RadiusLog):
		
		class Meta:
    		app_label = 'my_app'