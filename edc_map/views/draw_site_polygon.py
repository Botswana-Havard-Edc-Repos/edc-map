from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def draw_site_polygon(request, **kwargs):
    """Plots items from edc.base selection criteria.

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
        action_script_url_name = 'map_add_cart_url'
        has_items = False
        identifiers = request.session.get('identifiers', [])
        selected_section = request.POST.get(mapper.section_field_attr)
        cart_size = len(identifiers)
        cso_icon_dict = []
        section_color_code_list = []
        selected_region = request.POST.get(mapper.region_field_attr)
        request.session['icon'] = request.POST.get('marker_icon')
        if selected_section == 'All':
            pass
        else:
            pass
        payload = ()
        if selected_section != "ALL":
            for lon, lat, identifier_label, icon, other_identifier_label in payload:
                icon_name_length = len(icon)
                icon_label = icon[icon_name_length - 1]
                #print icon_label
                cso_icon_dict.append([icon_label, other_identifier_label])
        if selected_section == "All":
            section_color_codes = mapper.make_dictionary(mapper.other_icons, mapper.sections)
        else:
            section_color_codes = mapper.make_dictionary(mapper.icons, mapper.sections)
        for key_color, sec_value in section_color_codes.iteritems():
            section_color_code_list.append([key_color[:-1], sec_value])
        has_items = True
        payload_empty =True
        gps_coordinates = []
        landmark_list = []
        landmarks = mapper.landmarks
        for place, lat, lon in landmarks:
            landmark_list.append([place, lat, lon])
        return render_to_response(
            template, {
                'region_field_attr': mapper.region_field_attr,
                'section_field_attr': mapper.section_field_attr,
                'mapper_name': mapper_name,
                'payload': payload,
                'gps_coordinates': gps_coordinates,
                'action_script_url_name': action_script_url_name,
                'identifier_field_attr': mapper.identifier_field_attr,
                'has_items': has_items,
                'mapper_item_label': mapper_item_label,
                'gps_center_lat': mapper.gps_center_lat,
                'gps_center_lon': mapper.gps_center_lon,
                'selected_region': selected_region,
                'selected_icon': request.session['icon'],
                'icons': mapper.icons,
                'option': 'plot',
                'show_map': 1,
                'payload_empty': payload_empty,
                'identifiers': identifiers,
                'landmarks': landmark_list,
                'cart_size': cart_size,
                'cso_icon_dict': cso_icon_dict,
                'section_color_code_list': section_color_code_list,
                'selected_section': selected_section
                },
                context_instance=RequestContext(request)
            )
