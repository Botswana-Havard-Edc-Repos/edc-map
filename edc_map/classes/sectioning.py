from .controller import site_mappers


class Sectioning(object):

    def prepare_map_points(self, items, icon="blu-circle.png", selected_section="All", selected_sub_section='ALL'):

        locations_markers = []
        mapper_name = site_mappers.current_community
        mapper = site_mappers.get_mapper(mapper_name)
        for item in items:
            locations_markers.append(
                [
                    float(item.gps_target_lat),
                    float(item.gps_target_lon),
                    getattr(item, mapper.identifier_field_attr),
                    icon
                ]
            )
        return locations_markers
