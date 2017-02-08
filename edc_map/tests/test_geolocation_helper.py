from django.test import TestCase

from ..geolocation_helper import GeolocationHelper


class TestGeolocationHelper(TestCase):

    def setUp(self):
        self.geolocation_helper = GeolocationHelper()

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
            self.assertTrue(
                self.geolocation_helper.polygon_contains_point(
                    polygon, gps_lat, gps_lon))

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
        self.assertFalse(
            self.geolocation_helper.polygon_contains_point(
                polygon, gps_lat, gps_lon))

    def test_distance_btwn_points(self):
        """Assert that the correct distance between points is returned."""
        lat = -24.651352
        lon = 25.908847
        lat_2 = -24.644726
        lon_2 = 25.899749
        distance = self.geolocation_helper.points_distance(
            lat, lon, lat_2, lon_2)
        self.assertEqual(distance, 1.18)
