from django.contrib.admin import AdminSite


class EdcMapAdminSite(AdminSite):
    site_title = 'Edc Map'
    site_header = 'Edc Map'
    index_title = 'Edc Map'
    site_url = '/edc_map/list/'


edc_map_admin = EdcMapAdminSite(name='edc_map_admin')
