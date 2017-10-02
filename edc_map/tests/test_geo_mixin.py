import geopy

from django.test import TestCase

from ..geo_mixin import GeoMixin


class TestGeoMixin(TestCase):

    def setUp(self):
        self.geo_mixin = GeoMixin()

    def test_points_in_polygon(self):
        """Check if a point is in a polygon."""
        gps_lat = -24.644726
        gps_lon = 25.899749
        polygon = [
            [-24.64589, 25.8851],
            [-24.647, 25.88673],
            [-24.64969, 25.88866],
            [-24.65146, 25.89131],
            [-24.65354, 25.89502],
            [-24.65593, 25.90044],
            [-24.64916, 25.90322],
            [-24.64077, 25.90672],
            [-24.63772, 25.90171],
            [-24.63241, 25.89701],
            [-24.64224, 25.88709]]
        point = geopy.Point(float(gps_lat), float(gps_lon))
        self.assertTrue(
            self.geo_mixin.polygon_contains_point(
                polygon, point))

    def test_points_outside_polygon(self):
        """Check if a point is outside a polygon."""

        gps_lat = -24.651352
        gps_lon = 25.908847
        polygon = [
            [-24.64589, 25.8851],
            [-24.647, 25.88673],
            [-24.64969, 25.88866],
            [-24.65146, 25.89131],
            [-24.65354, 25.89502],
            [-24.65593, 25.90044],
            [-24.64916, 25.90322],
            [-24.64077, 25.90672],
            [-24.63772, 25.90171],
            [-24.63241, 25.89701],
            [-24.64224, 25.88709]]
        point = geopy.Point(float(gps_lat), float(gps_lon))
        self.assertFalse(
            self.geo_mixin.polygon_contains_point(
                polygon, point))

    def test_distance_btwn_points(self):
        """Assert that the correct distance between points is returned."""
        lat = -24.651352
        lon = 25.908847
        lat_2 = -24.644726
        lon_2 = 25.899749
        point_a = geopy.Point(float(lat), float(lon))
        point_b = geopy.Point(lat_2, lon_2)
        distance = self.geo_mixin.distance_between_points(point_a, point_b)
        self.assertEqual(round(distance, 2), 1.18)
