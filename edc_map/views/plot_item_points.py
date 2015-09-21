from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from ..classes import site_mappers
from ..exceptions import MapperError


def plot_item_points(request, **kwargs):
    """Plot items from edc.base selection criteria.

      * Filter points to plot by sending coordinates of a selected ward only to the items.html template.
      * Regions contain sections    """
    # TODO: difference in ward ward section selected section and section ??? very confusing
            # docstring Comment is out of date?
    template = 'map.html'
    mapper_item_label = kwargs.get('mapper_item_label', '')
    mapper_name = kwargs.get('mapper_name', '')

    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_item_label))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        action_script_url = 'map_add_cart_url'
        has_items = False
        identifiers = request.session.get('identifiers', [])
        selected_sub_section = request.POST.get(mapper.section_field_attr)
        selected_randomization = request.POST.get(mapper.item_selected_field)
        if selected_randomization == 'twenty_percent':
            selected_randomization = 1
        if selected_randomization == 'five_percent':
            selected_randomization = 2
        cart_size = len(identifiers)
        section_color_code_list = []
        selected_region = request.POST.get(mapper.region_field_attr)
        request.session['icon'] = request.POST.get('marker_icon')
        if selected_region == 'All':
            if selected_sub_section == 'All':
                items = mapper.item_model.objects.filter(Q(**{mapper.item_selected_field: selected_randomization}))
            else:
                items = mapper.item_model.objects.filter(
                    Q(**{mapper.section_field_attr: selected_sub_section, mapper.item_selected_field: 1}) |
                    Q(**{'{0}__in'.format(mapper.identifier_field_attr): identifiers, mapper.item_selected_field: selected_randomization}))
        else:
            if selected_sub_section == 'All':
                items = mapper.item_model.objects.filter(
                Q(**{mapper.region_field_attr: selected_region, mapper.item_selected_field: selected_randomization}) |
                Q(**{'{0}__in'.format(mapper.identifier_field_attr): identifiers, mapper.item_selected_field: selected_randomization}))
            else:
                items = mapper.item_model.objects.filter(
                Q(**{mapper.region_field_attr: selected_region, mapper.section_field_attr: selected_sub_section, mapper.item_selected_field: selected_randomization}) | 
                Q(**{'{0}__in'.format(mapper.identifier_field_attr): identifiers, mapper.section_field_attr: selected_sub_section, mapper.item_selected_field: selected_randomization}))
        icon = str(request.session['icon'])
        payload = mapper.prepare_map_points(items,
            icon,
            identifiers,
            'egg-circle.png',
            'red-circle', selected_region, selected_sub_section)
        if selected_sub_section == "All":
            section_color_codes = {'Teal':'A', 'Yellow': 'B', 'Orange': 'C', 'Pink': 'D'}
        else:
            section_color_codes = mapper.make_dictionary(mapper.sections, mapper.other_icons)
        for key_color, sec_value in section_color_codes.iteritems():
            section_color_code_list.append([key_color, sec_value])
        if payload:
            has_items = True
        landmark_list = []
        landmarks = mapper.landmarks
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        return render_to_response(
            template, {
                'item_region_field': mapper.region_field_attr,
                'section_field_attr': mapper.section_field_attr,
                'mapper_name': mapper_name,
                'payload': payload,
                'action_script_url': action_script_url,
                'identifier_field_attr': mapper.identifier_field_attr,
                'has_items': has_items,
                'mapper_item_label': mapper_item_label,
                'selected_region': selected_region,
                'selected_icon': request.session['icon'],
                'icons': mapper.icons,
                'option': 'plot',
                'gps_center_lat': mapper.gps_center_lat,
                'gps_center_lon': mapper.gps_center_lon,
                'show_map': 1,
                'identifiers': identifiers,
                'landmarks': landmark_list,
                'cart_size': cart_size,
                'section_color_code_list': section_color_code_list,
                'selected_sub_section': selected_sub_section
                },
                context_instance=RequestContext(request)
            )
