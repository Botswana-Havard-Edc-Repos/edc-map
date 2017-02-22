from django.conf.urls import url, include

from edc_base.views import LogoutView, LoginView


from .views import MapImageView, ItemDivisionsView, HomeView, CreateContainers, ItemsToGps
from .admin_site import edc_map_admin

urlpatterns = [
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)/(?P<zoom_level>[1-9]{1})', MapImageView.as_view(), name='map_image_url'),
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)$', MapImageView.as_view(), name='map_image_url'),
    url(r'^draw_container/(?P<map_area>\w+)/$', ItemDivisionsView.as_view(), name='item_division_url'),
    url(r'^save_container/(?P<map_area>\w+)/$', CreateContainers.as_view(), name='save_container_url'),
    url(r'^items_to_gps/(?P<map_area>\w+)/$', ItemsToGps.as_view(), name='items_to_gps_url'),
    url(r'^edc/', include('edc_base.urls', 'edc-base')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^admin/', edc_map_admin.urls),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(
        pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
