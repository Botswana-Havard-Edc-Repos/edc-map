from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminReadOnlyMixin, ModelAdminAuditFieldsMixin)

from .admin_site import edc_map_admin
from .forms import ContainerForm, InnerContainerForm
from .models import Container, InnerContainer


class ModelAdminMixin(ModelAdminFormInstructionsMixin,
                      ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin,
                      ModelAdminReadOnlyMixin,
                      admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(Container, site=edc_map_admin)
class ContainerAdmin(ModelAdminMixin):

    form = ContainerForm
    list_per_page = 10

    list_display = ('name', 'map_area', 'created', 'modified')

    list_filter = (
        'created',
        'modified',
        'map_area',
        'hostname_modified')

    search_fields = ('map_area', 'id')


@admin.register(InnerContainer, site=edc_map_admin)
class InnerContainerAdmin(ModelAdminMixin):

    form = InnerContainerForm
    list_per_page = 10

    list_display = ('map_area', 'device_id', 'name', 'created', 'modified')

    list_filter = (
        'created',
        'modified',
        'name',
        'hostname_modified')

    search_fields = ('device_id', 'name', 'id')
