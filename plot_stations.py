import math
import sys
from state_mapper import Mapper
from geospacial_methods import stringToCoordinates

data_file_path = 'Data/FM_service_contour_current.txt'
data_file = open(data_file_path,'r')
state = 'usa'

if __name__ == '__main__':
    m = Mapper(state)
    for line_num, line in enumerate(data_file):
        if line_num%1000 == 0:
            print line_num
        line.rstrip()
        station_raw = line.split('|')
        for i in range(0, len(station_raw)):
            station_raw[i] = station_raw[i].rstrip()
        station_loc = stringToCoordinates(station_raw[3])
        m.plotPoint(station_loc[1], station_loc[0])
    m.displayMap()
