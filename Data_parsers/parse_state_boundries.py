#!/usr/bin/python
# -*- coding: utf-8 -*-
#only works for the NW quadrant
import re
import codecs

#Adapted from 
#http://infohost.nmt.edu/tcc/help/lang/python/mapping/terrapos.py
def dmDeg(degree, minute, direction):
    sign = 1.0
    if  direction == 'S' or direction == 'W':
        sign = -1.0

    return sign*(degree+(minute/60.0))

file_loc = 'state_boundries_raw.txt'
search_string = u"(\d+)\u00b0( (\d+)')? ([WENS]) to "+\
        u"(\d+)\u00b0( (\d+)')? ([WENS])" 
f = codecs.open(file_loc, encoding='utf-8')

print '#State,lllon,urlon,lllat,urlat'
output = ''
line_count = 0

for line in f:
    line = line.rstrip()

    if len(line) == 0 or line[0] == '#' or line[0:4] == 'http':
        continue

    if line_count == 0:
        output = line+','

    else:
        re_res = re.search(search_string, line)
        ll_deg, ll_min, ll_dir= \
                int(re_res.group(1)), re_res.group(3), re_res.group(4)
        ll_min = int(ll_min) if ll_min else 0

        ur_deg, ur_min, ur_dir= \
                int(re_res.group(5)), re_res.group(7), re_res.group(8)
        ur_min = int(ur_min) if ur_min else 0
        output += str(dmDeg(ll_deg, ll_min, ll_dir))+','
        output += str(dmDeg(ur_deg, ur_min, ur_dir))

        if line_count == 1:
            output += ','
        else:
            print output


    line_count = (line_count+1)%3

