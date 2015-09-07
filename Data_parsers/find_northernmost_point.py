import math
import sys

data_file_path = '../Data/FM_service_contour_current.txt'
data_file = open(data_file_path,'r')

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

northernmost_point = None
for line_num, line in enumerate(data_file):
    if line_num % 1000 == 0:
        print line_num // 1000
    line.rstrip()
    station_raw = line.split('|')
    for i in range(0, len(station_raw)):
        station_raw[i] = station_raw[i].rstrip()
    station_loc = stringToCoordinates(station_raw[3])

    contour_points = [(0,0) for i in range(0, len(station_raw) - 5)]
    for coord_num in range(0, len(contour_points) - 2):
        new_coord = stringToCoordinates(station_raw[coord_num + 4])
        if northernmost_point == None or\
                northernmost_point[0] < new_coord[0]:
           northernmost_point = new_coord 
            

print northernmost_point
