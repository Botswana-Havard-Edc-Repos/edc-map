from math import sin, cos, radians, degrees, acos


def calc_dist(lat_a, long_a, lat_b, long_b):
    """Calculate distance between two geographic points

        Using latitude and longitude of two points calculate distance between points
        and return the distance in miles.
    """
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    return degrees(acos(distance)) * 69.09


def get_longitude(gps_s, longitude):
    lon = None
    if gps_s and longitude:
        gps_s = float(gps_s)
        longitude = float(longitude)
        lon = round((gps_s) + (longitude / 60), 5)
    return lon


def get_latitude(gps_e, latitude):
    lat = None
    if gps_e and latitude:
        gps_e = float(gps_e)
        latitude = float(latitude)
        lat = -1 * round((gps_e) + (latitude / 60), 5)
    return lat
