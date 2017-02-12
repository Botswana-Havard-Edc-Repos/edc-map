from django.contrib import admin
from django.contrib.auth.models import User

from .admin_site import edc_map_admin
from .forms import MapDivisionForm
from .models import MapDivision


@admin.register(MapDivision, site=edc_map_admin)
class HouseholdAdmin(admin.ModelAdmin):

    form = MapDivisionForm
    list_select_related = ('user', )
    list_per_page = 10

    list_display = ('label', 'map_area', 'created', 'modified')

    list_filter = ('created', 'modified', 'label', 'map_area', 'hostname_modified')

    search_fields = ('label', 'map_area', 'id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            if request.GET.get('user'):
                kwargs["queryset"] = User.objects.filter(
                    id__exact=request.GET.get('user', 0))
        return super(HouseholdAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
