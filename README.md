[![Django CI](https://github.com/Botswana-Havard-Edc-Repos/edc-map/actions/workflows/django.yml/badge.svg)](https://github.com/Botswana-Havard-Edc-Repos/edc-map/actions/workflows/django.yml) [![Coverage Status](https://coveralls.io/repos/github/botswana-harvard/edc-map/badge.svg?branch=develop)](https://coveralls.io/github/botswana-harvard/edc-map?branch=develop)
[![Coverage Status](https://coveralls.io/repos/github/Botswana-Havard-Edc-Repos/edc-map/badge.svg?branch=develop)](https://coveralls.io/github/Botswana-Havard-Edc-Repos/edc-map?branch=develop)

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
