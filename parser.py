import math
import sys

data_file_path = 'Data/FM_service_contour_current.txt'
data_file = open(data_file_path, 'r')

def stringToCoordinates(coord_string):
    coord_array = coord_string.split(',')
    for i in (0, 1):
        coord_array[i] = coord_array[i].rstrip()
    coord_tuple = (float(coord_array[0]), float(coord_array[1]))
    return coord_tuple

def coordinateDistance(coord_1, coord_2):#Haversine formula
    earth_radius = 6371000 #meters
    lat_1, long_1 = coord_1
    lat_2, long_2 = coord_2
    lat_rad_1, lat_rad_2 = math.radians(lat_1), math.radians(lat_2)
    lat_delta = math.radians(lat_2 - lat_1)
    long_delta = math.radians(long_2 - long_1)

    a = math.sin(lat_delta/2)**2 + math.cos(lat_rad_1)*math.cos(lat_rad_2) * \
            math.sin(long_delta)**2
    c = math.atan2(math.sqrt(a),math.sqrt(1-a))

    return earth_radius * c

for line_num, line in enumerate(data_file):
    line.rstrip()
    station_raw = line.split('|')
    for i in range(0, len(station_raw)):
        station_raw[i] = station_raw[i].rstrip()
    station_type = station_raw[1]
    station_id = station_raw[2]
    station_id = station_id.split()
    call_sign = station_id[0]
    application_file_number = station_id[1]
    station_loc = stringToCoordinates(station_raw[3])

    contour_points = [(0,0) for i in range(0, len(station_raw) - 5)]
    max_distance = None
    max_distance_pair = None
    for coord_num in range(0, len(contour_points) - 2):
        new_coord = stringToCoordinates(station_raw[coord_num + 4])
        distance = coordinateDistance(new_coord, station_loc)
        if max_distance == None or distance > max_distance:
            max_distance = distance
            max_distance_pair = new_coord
        contour_points[coord_num - 4] = new_coord
