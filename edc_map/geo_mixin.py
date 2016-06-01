from geopy import Point, distance


class GeoMixin:

    gps_center_lat = None
    gps_center_lon = None

    def gps_distance_between_points(self, lat, lon, center_lat=None, center_lon=None):
        """Check if a GPS point is within the boundaries of a community

        This method uses geopy.distance and geopy.Point libraries to
        calculate the distance between two points and return the
        distance in units requested.

        The community_radius, community_center_lat and
        community_center_lon are from the Mapper class of each community.
        """
        center_lat = center_lat or self.gps_center_lat
        center_lon = center_lon or self.gps_center_lon
        pt1 = Point(float(lat), float(lon))
        pt2 = Point(float(center_lat), float(center_lon))
        dist = distance.distance(pt1, pt2).km
        return dist

    def deg_to_dms(self, deg):
        """Convert a latitude or longitude into degree minute GPS format
        """
        d = int(deg)
        md = (deg - d) * 60
        m = round(md, 3)
        if d < 0 and m < 0:
            d = -d
            m = -m
        return [d, m]

    def gps(self, direction, degrees, minutes):
        """Converts GPS degree/minutes to latitude or longitude."""
        dct = {'s': -1, 'e': 1}
        if direction not in dct.keys():
            raise TypeError('Direction must be one of {0}. Got {1}.'.format(dct.keys(), direction))
        d = float(degrees)
        m = float(minutes)
        return dct[direction] * round((d) + (m / 60), 5)

    def gps_lat(self, d, m):
        """Converts degree/minutes S to latitude."""
        return self.gps('s', d, m)

    def gps_lon(self, d, m):
        """Converts degree/minutes E to longitude."""
        return self.gps('e', d, m)
