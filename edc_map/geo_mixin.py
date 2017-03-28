from geopy.distance import vincenty

from .exceptions import MapperError


class GeoMixin:

    def polygon_contains_point(self, polygon, point):
        """Return True if a point is inside a polygon."""

        n = len(polygon)
        inside = False
        latitude = point.lat
        longitude = point.lon
        latitude_x, latitude_y = polygon[0]
        for i in range(n + 1):
            latitude_x2, latitude_y2 = polygon[i % n]
            if longitude > min(latitude_y, latitude_y2):
                if longitude <= max(latitude_y, latitude_y2):
                    if latitude <= max(latitude_x, latitude_x2):
                        if latitude_y != latitude_y2:
                            xinters = (longitude - latitude_y) * (latitude_x2 - latitude_x) / (latitude_y2 - latitude_y) + latitude_x
                        if latitude_x == latitude_x2 or latitude <= xinters:
                            inside = not inside
            latitude_x, latitude_y = latitude_x2, latitude_y2
        return inside

    def distance_between_points(self, point_a, point_b, units=None):
        """Return distance between two points (vincenty, default units=km)."""
        units = units or 'km'
        return getattr(vincenty(point_a, point_b), units)

    def point_in_radius(self, point, center_point, radius, units=None):
        """Return True if point is within radius."""
        units = units or 'km'
        d = self.distance_between_points(point, center_point, units)
        return d <= radius

    def raise_if_not_in_polygon(self, polygon, point):
        """Raises an exception if point not within a polygon."""
        if not self.polygon_contains_point(polygon, point):
            raise MapperError(
                'GPS ({point.latitude}, {point.longitude}) is outside the expected polygon.'.format(point=point))

    def raise_if_not_in_radius(self, point, center_point, radius, units=None,
                               label=None):
        """Raises an exception if point is not within radius (default units=km)."""
        label = label or ''
        units = units or 'km'
        if not self.point_in_radius(point, center_point, radius, units):
            d = self.distance_between_points(point, center_point, units)
            d = round(d, 2)
            raise MapperError(
                'GPS ({point.latitude}, {point.longitude}) is more than {radius}{units} '
                'from {label} ({center_point.latitude}, {center_point.longitude}). '
                'Got {distance}{units}.'.format(
                    point=point, radius=radius, center_point=center_point,
                    distance=d, units=units, label=label))

    def deg_to_dms(self, deg):
        """Convert latitude or longitude into degree minute GPS format."""
        d = int(deg)
        md = (deg - d) * 60
        m = round(md, 3)
        if d < 0 and m < 0:
            d = -d
            m = -m
        return [d, m]

    def gps_lat(self, d, m):
        """Converts degree/minutes S to latitude."""
        return self.gps('s', d, m)

    def gps_lon(self, d, m):
        """Converts degree/minutes E to longitude."""
        return self.gps('e', d, m)

    def gps(self, direction, degrees, minutes):
        """Converts GPS degree/minutes to latitude or longitude."""
        dct = {'s': -1, 'e': 1}
        if direction not in dct.keys():
            raise TypeError('Direction must be one of {0}. Got {1}.'.format(dct.keys(), direction))
        d = float(degrees)
        m = float(minutes)
        return dct[direction] * round((d) + (m / 60), 5)
