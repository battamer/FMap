import math

def stringToCoordinates(coord_string):
    coord_array = coord_string.split(',')
    for i in (0, 1):
        coord_array[i] = coord_array[i].rstrip()
    coord_tuple = (float(coord_array[0]), float(coord_array[1]))
    return coord_tuple

def coordinateDistance(coord_1, coord_2):#Haversine formula
    earth_radius_m = 6371000
    lat_1, long_1 = coord_1
    lat_2, long_2 = coord_2
    lat_rad_1, lat_rad_2 = math.radians(lat_1), math.radians(lat_2)
    lat_delta = math.radians(lat_2 - lat_1)
    long_delta = math.radians(long_2 - long_1)

    a = math.sin(lat_delta/2)**2 + math.cos(lat_rad_1)*math.cos(lat_rad_2) * \
            math.sin(long_delta)**2
    c = math.atan2(math.sqrt(a),math.sqrt(1-a))

    return earth_radius_m * c 

def coordinateGridLoc(lat, lon):
    if lat <= 0:
        lat = abs(lat) + 180
    if lon <= 0:
        lon = abs(lon) + 180
    lat, lon = lat//2, lon//4

    return lat, lon