from django.conf.urls import patterns, url
from .classes import site_mappers
from .views import (item_map, add_to_cart, update_cart, checkout_cart, save_cart, kmz_file_upload, create_kmz_items,
                    plot_item_points, set_section, set_sub_section, save_section, save_sub_section,
                    clear_section, clear_sub_section, clear_sub_section_index, clear_all_sections,
                    upload_item_map, map_section, map_sub_sections, db_update, db_update_index,
                    dispatch_to_gps_index, coordinates_to_gps, map_index)

urlpatterns = patterns('',
    url(r'^item_map/(?P<mapper_name>\w+)/(?P<identifier>[a-zA-Z0-9_-]+)/(?P<lon>[a-z0-9\.\-\:]+)/(?P<lat>[a-z0-9\.\-\:]+)/(?P<saved>saved)/',
        item_map,
        name='item_map_url'),
    url(r'^item_map/(?P<mapper_name>\w+)/(?P<identifier>[a-zA-Z0-9_-]+)/(?P<lon>[a-z0-9\.\-\:]+)/(?P<lat>[a-z0-9\.\-\:]+)/',
        item_map,
        name='item_map_url'),
    url(r'^item_map/(?P<mapper_name>\w+)/(?P<identifier>[a-zA-Z0-9_\-]+)/',
        item_map,
        name='item_map_url'),
    url(r'^item_map/(?P<mapper_name>\w+)/',
        item_map,
        name='item_map_url'),

    url(r'^add_cart/(?P<mapper_name>\w+)/', add_to_cart, name='map_add_cart_url'),
    url(r'^update_cart/(?P<mapper_name>\w+)/', update_cart, name='update_identifier_cart'),
    url(r'^checkout/(?P<mapper_name>\w+)/', checkout_cart, name='map_checkout_cart_url'),
    url(r'^complete/(?P<mapper_name>\w+)/', save_cart, name='complete_cart_save'),
    url(r'^upload_kmz/(?P<mapper_name>\w+)/', kmz_file_upload, name='kmz_file_upload_url'),
    url(r'^create_kmz_itemsdata_list.pop[0]/(?P<mapper_name>\w+)/', create_kmz_items,
        name='create_kmz_items_url'),
    url(r'^view/(?P<mapper_name>\w+)/', plot_item_points, name='map_plot_item_points_url'),
    url(r'^set_section/(?P<mapper_name>\w+)/', set_section, name='set_section_url'),
    url(r'^set_sub_section/(?P<mapper_name>\w+)/', set_sub_section, name='set_sub_section_url'),
    url(r'^save_section/(?P<mapper_name>\w+)/', save_section, name='save_section_url'),
    url(r'^save_sub_section/(?P<mapper_name>\w+)/', save_sub_section, name='save_sub_section_url'),
    url(r'^clear_section/(?P<mapper_name>\w+)/', clear_section, name='clear_section_url'),
    url(r'^clear_sub_section/(?P<mapper_name>\w+)/', clear_sub_section, name='clear_sub_section_url'),
    url(r'^clear_sub_section_index/(?P<mapper_name>\w+)/', clear_sub_section_index,
        name='clear_sub_section_index_url'),
    url(r'^clear_all_sections/(?P<mapper_name>\w+)/', clear_all_sections, name='clear_all_sections_url'),
    url(r'^upload_item_map/(?P<mapper_name>\w+)/', upload_item_map, name='upload_item_map_url'),
    url(r'^map_section/(?P<mapper_name>\w+)/', map_section, name='map_section_url'),
    url(r'^map_sub_sections/(?P<mapper_name>\w+)/', map_sub_sections, name='map_sub_sections_url'),
    url(r'^db_update/(?P<mapper_name>\w+)/', db_update, name='map_db_update'),
    url(r'^gps_point_update/(?P<mapper_name>\w+)/', db_update_index, name='map_gps_point_update_url'),
    url(r'dispatch_to_gps_index/(?P<mapper_name>\w+)/', dispatch_to_gps_index, name='dispatch_to_gps_index_url'),
    url(r'coordinates_to_gps/(?P<mapper_name>\w+)/', coordinates_to_gps, name='coordinates_to_gps_url'),
)

for mapper_name in site_mappers.get_registry().iterkeys():
    urlpatterns += patterns('', url(r'^(?P<mapper_name>{0})/$'.format(mapper_name), map_index,
                                    name='selected_map_index_url'))

urlpatterns += patterns('', url(r'^', map_index, name='map_index_url'))
