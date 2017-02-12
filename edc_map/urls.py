from django.conf.urls import url, include

from edc_base.views import LogoutView, LoginView


from .views import MapImageView, DrawClusterMixin, HomeView, SaveCluster
from .admin_site import edc_map_admin

urlpatterns = [
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)/(?P<zoom_level>[1-9]{1})', MapImageView.as_view(), name='map_image_url'),
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)$', MapImageView.as_view(), name='map_image_url'),
    url(r'^draw_polygon/(?P<map_area>\w+)/$', DrawClusterMixin.as_view(), name='draw_cluster_url'),
    url(r'^save_cluster/(?P<map_area>\w+)/$', SaveCluster.as_view(), name='save_cluster_url'),
    url(r'^edc/', include('edc_base.urls', 'edc-base')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^admin/', edc_map_admin.urls),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(
        pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
