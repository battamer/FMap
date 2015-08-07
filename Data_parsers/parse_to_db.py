import math
import sys
import sqlite3 as lite
import pickle

data_file_path = '../Data/FM_service_contour_current.txt'
db_loc = '../Data/fmdb.db'
sql = {'create_stations_table' : 
            'CREATE TABLE Stations\
            (Station_ID         TEXT    NOT NULL,\
             Transmitter_Lat    REAL    NOT NULL,\
             Transmitter_Lon    REAL    NOT NULL,\
             Max_range          REAL    NOT NULL,\
             Grid_loc_lat       INT     NOT NULL,\
             Grid_loc_lon       INT     NOT NULL,\
             Waypoints          TEXT    NOT NULL);',
        'drop_stations_table' :
            'DROP TABLE IF EXISTS Stations;',
        }
            

def stationsInsertQuery(station_id, lat, lon, max_range, waypoints):
    grid_loc_lat, grid_loc_lon = coordinateGridLoc(lat, lon)
    query = 'INSERT INTO Stations VALUES \
                ("%s", %s, %s, %s, %s, %s, "%s");' % \
                (station_id, lon, lat, max_range, 
                        grid_loc_lat, grid_loc_lon, waypoints)
    return query


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
with lite.connect(db_loc) as con:
    cur = con.cursor()
    cur.execute(sql['drop_stations_table'])
    cur.execute(sql['create_stations_table'])

    with open(data_file_path,'r') as data_file:
        for line_num, line in enumerate(data_file):
            if line_num % 1000 == 0:
                print line_num // 1000
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

            
            waypoints = map(lambda x: stringToCoordinates(x),
                                station_raw[4 : len(station_raw) - 3])
            max_distance = None
            max_distance_pair = None
            for waypoint in waypoints:
                distance = coordinateDistance(waypoint, station_loc)
                if max_distance == None or distance > max_distance:
                    max_distance = distance
                    max_distance_pair = waypoint 

            waypoints_pickled = pickle.dumps(waypoints)
            cur.execute(stationsInsertQuery(
                            call_sign, station_loc[0], 
                            station_loc[1], max_distance, waypoints_pickled))
