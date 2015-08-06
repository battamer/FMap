import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math

state_boundries_file_loc = 'Data/stateboundries.csv'
states_shapefile_loc = 'Data/States_shapefiles/tl_2014_us_state'

class Mapper:
    def __init__(self, state):
        with open(state_boundries_file_loc) as f:
            for line in f:
                line = line.rstrip().split(',')
                if line[0].lower() == state.lower():
                    ll_lon, ll_lat = float(line[1]), float(line[3])
                    ur_lon, ur_lat = float(line[2]), float(line[4])
                    center_lon = ll_lon + ur_lon
                    if math.copysign(1, ll_lon) != math.copysign(1, ur_lon):
                        center_lon = -180 + center_lon
                    else:
                        center_lon = center_lon / 2
                    center_lat = (ll_lat + ur_lat) / 2

                    self.m = Basemap(llcrnrlon = ll_lon, llcrnrlat = ll_lat,
                                urcrnrlon = ur_lon, urcrnrlat = ur_lat,
                                projection = 'lcc', lat_1 = center_lat,
                                lon_0 = center_lon)
                    self.m.readshapefile(states_shapefile_loc,
                                        'states', drawbounds = True)
                    plt.show()
    


if __name__ == '__main__':
    m = Mapper('USA')
