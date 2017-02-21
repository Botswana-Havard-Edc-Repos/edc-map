from django.contrib import admin

from .admin_site import edc_map_admin
from .forms import ContainerForm, InnerContainerForm
from .models import Container, InnerContainer


@admin.register(Container, site=edc_map_admin)
class ContainerAdmin(admin.ModelAdmin):

    form = ContainerForm
    list_per_page = 10

    list_display = ('container_name', 'map_area', 'created', 'modified')

    list_filter = (
        'created',
        'modified',
        'map_area',
        'hostname_modified')

    search_fields = ('map_area', 'id')


@admin.register(InnerContainer, site=edc_map_admin)
class InnerContainerAdmin(admin.ModelAdmin):

    form = InnerContainerForm
    list_per_page = 10

    list_display = ('username', 'inner_container_name', 'created', 'modified')

    list_filter = (
        'created',
        'modified',
        'inner_container_name',
        'hostname_modified')

    search_fields = ('username', 'inner_container_name', 'id')
