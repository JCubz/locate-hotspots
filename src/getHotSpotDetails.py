import csv
# argv[1] = hotspots
# argv[2] = rectangle coordinates

import sys
import xml.etree.ElementTree as ET
import os

from rectangles import Rectangle, get_rectangle, get_column, get_direction
from coordinate import Coordinate

# from utilities import import_rectangles, import_hotspots
r = []
try:
    # Loads up the rectangles into r[]
    # f = open(sys.argv[2], 'rt')
    # rectangleInputFile = csv.reader(f)
    if 'nt' in os.name:
        file_seperator = '\\'
    else:
        file_seperator = '/'

    if len(sys.argv) > 3:
        flight = sys.argv[2]
        panel_space = float(sys.argv[3])
    else:
        print 'Please give name of Flight'
    tree = ET.parse(str(sys.argv[1]) + 'CoordinateFiles' + file_seperator + flight + '.xml')
    svg = tree.getroot()
    # Parse and create Rectangle
    for polygon in svg:
        if 'polygon' in polygon.tag:
            name = polygon.get('id')
            gap_space = float(polygon.get('gap'))
            p = map(float, polygon.get('points').split())
            tr = Coordinate(p[0], p[1])
            br = Coordinate(p[2], p[3])
            bl = Coordinate(p[4], p[5])
            tl = Coordinate(p[6], p[7])
            r.append(Rectangle(name, tl, tr, bl, br, panel_space, gap_space))
            #print 'loaded rectangle ' + name

    print ''
    print 'loading file ' + str(sys.argv[1]) + 'CoordinateFiles' + file_seperator + 'SolarEyeFaults' + flight + '.csv'
    f = open((str(sys.argv[1]) + file_seperator + 'CoordinateFiles' + file_seperator + 'SolarEyeFaults' + flight + '.csv'), 'rt')
    hotpots = csv.reader(f)
    fw = open((str(sys.argv[1]) + 'target' + file_seperator + flight + 'Output.csv'), 'wb+')
    fe = open((str(sys.argv[1]) + 'target' + file_seperator + flight + 'ErrorRows.csv'), 'wb+')

    writer = csv.writer(fw)
    writer_e = csv.writer(fe)
    writer.writerow(('OriginX value', 'OriginY value', 'Lat', 'Long', 'Row letter', 'Column number', 'North/South'))
    for row in hotpots:
        try:
            float(row[0])  # will give error if the coordinate is not a float
            newHotSpot = Coordinate(row[0], row[1])
            hs_rect = get_rectangle(r, newHotSpot)
            hs_line = get_column(hs_rect, newHotSpot)
            hs_dir = get_direction(hs_rect, newHotSpot)
            # print '-Hot spot in Longitude and Latitude- ' + str(row[4]) + '    ' + str(row[5])
            # print 'Rectangle: ' + hs_rect.name
            # print 'Line: ' + str(hs_line)
            # print 'Direction ' + hs_dir
            # print ''
            if hs_line is -1:
                print 'Error at Line'
                print '-Hot spot in Longitude and Latitude- ' + str(row[4]) + '    ' + str(row[5])
                print 'Rectangle: ' + hs_rect.name
                print 'Direction ' + hs_dir
                print ''
                writer_e.writerow((row[0], row[1], row[4], row[5], hs_rect.name, str(hs_line), hs_dir))
            else:
                writer.writerow((row[0], row[1], row[4], row[5], hs_rect.name, str(hs_line), hs_dir))

        except ValueError:
            if 'Ortho' not in row[0]:  # Ortho is in the first line that is the header for the csv
                print 'Error parsing hotspot-'
                print row



finally:
    f.close()
    fe.close()
    fw.close()