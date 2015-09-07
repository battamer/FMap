import math
import sys
import sqlite3 as lite
import pickle
from state_mapper import Mapper
from geospacial_methods import coordinateGridLoc, coordinateDistance

db_loc = 'Data/fmdb.db'
sql = 	{'select_by_grid': ('SELECT * FROM Stations WHERE '
						'Grid_loc_lat = %s AND '
						'Grid_loc_lon = %s;')
		}

if __name__ == '__main__':
	chas_sc_loc = (32.7833, -79.9333)
	state = 'south carolina'
	map = Mapper(state)

	with lite.connect(db_loc) as con:
		cur = con.cursor()
		lat_center_grid, lon_center_grid = coordinateGridLoc(*chas_sc_loc)
		lat_center_grid, lon_center_grid = \
							int(lat_center_grid), int(lon_center_grid)
		for lat_grid in range(lat_center_grid - 1, lat_center_grid + 2):
			for lon_grid in range(lon_center_grid - 1, lon_center_grid + 2):
				grid_select_query = sql['select_by_grid'] % \
										(lat_grid, lon_grid)
				cur.execute(grid_select_query)
				for row in cur:
					if row[3] < coordinateDistance(chas_sc_loc,\
										 (row[1], row[2])):
						map.plotPoint(row[1], row[2])
		map.setBorders()
		map.displayMap()