import math


class Coordinate(object):
    def __init__(self, xCoor, yCoor):
        self.x = float(xCoor)
        self.y = float(yCoor)


# gets the distance between two points in pixels
def get_distance(c1, c2):
    distance = abs(math.sqrt((c2.x - c1.x) ** 2 + (c2.y - c1.y) ** 2))
    return distance


# Gives the next coordinate to the right given a starting coordinate, the distance, and the slope
def next_coordinate_right(start_coordinate, dist, slope):
    y = ((slope ** 2) * (dist ** 2) / ((slope ** 2) + 1)) ** (.5)
    x = y / slope
    if slope < 0:
        y = 0 - y
    return Coordinate(start_coordinate.x + x, start_coordinate.y + y)

# Readd this if we decide to account for earth's circumfrance and use GPS
# from geopy.distance import vincenty
# if 'vincenty' in formula:
#	p1 = (c1.x, c1.y)
#	p2 = (c2.x, c2.y)
#	distance = vincenty(p1, p2).m

# else:
#	raise ValueError('Wrong formula inputed')
