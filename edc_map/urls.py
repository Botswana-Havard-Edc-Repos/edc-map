from django.conf.urls import url

from .views import MapImageView, DrawCluster

# from .views import (kmz_file_upload, create_kmz_items, map_index)

urlpatterns = [
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)/(?P<zoom_level>[1-9]{1})', MapImageView.as_view(), name='map_image_url'),
    url(r'^(?P<map_area>\w+)/(?P<pk>[^/]+)$', MapImageView.as_view(), name='map_image_url'),
    url(r'^draw_cluster/', DrawCluster.as_view(), name='draw_cluster_url'),
]

# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     url(r'^upload_kmz/(?P<mapper_name>\w+)/', kmz_file_upload, name='kmz_file_upload_url'),
#     url(r'^create_kmz_itemsdata_list.pop[0]/(?P<mapper_name>\w+)/', create_kmz_items,
#         name='create_kmz_items_url'),
#     url(r'^', SectioningView.as_view(), name='sectioning_view_url'),
# for mapper_name in site_mappers.map_areas:
#     urlpatterns += patterns('', url(r'^(?P<mapper_name>{0})/$'.format(mapper_name), map_index,
#                                     name='selected_map_index_url'))

# urlpatterns += patterns('', url(r'^', map_index, name='map_index_url'))
