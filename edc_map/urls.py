from django.conf.urls import include
from django.urls import re_path
from .admin_site import edc_map_admin
from .views import (
    MapImageView, ItemDivisionsView, HomeView, CreateContainers, ItemsToGps,
    ItemCilentAllocationView, ItemListView)

app_name = 'edc_map'

urlpatterns = [
    re_path(r'^edc/', include('edc_base.urls', 'edc-base')),
    re_path(r'^tz_detect/', include('tz_detect.urls')),
    re_path(r'^admin/', edc_map_admin.urls),
    re_path(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)/(?P<zoom_level>[1-9]{1})',
            MapImageView.as_view(), name='map_image_url'),
    re_path(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)$',
            MapImageView.as_view(), name='map_image_url'),
    re_path(r'^draw_polygon/(?P<map_area>\w+)/$',
            ItemDivisionsView.as_view(), name='item_division_url'),
    re_path(r'^save_polygon/(?P<map_area>\w+)/$',
            CreateContainers.as_view(), name='save_container_url'),
    re_path(r'^items_to_gps/(?P<map_area>\w+)/$',
            ItemsToGps.as_view(), name='items_to_gps_url'),
    re_path(
        r'^list_items/(?P<device_id>\w+)/(?P<container_name>\w+)/(?P<inner_container_name>\w+)/$',
        ItemListView.as_view(), name='items_list_url'),
    re_path(r'^item_client_allocation/$',
            ItemCilentAllocationView.as_view(), name='item_client_allocation_url'),
    re_path(r'^', HomeView.as_view(), name='home_url'),
]
