from coordinate import Coordinate, get_distance, next_coordinate_right


# import math

class Rectangle(object):
    # Needs Coordinate values
    def __init__(self, name, topLeft, topRight, bottomLeft, bottomRight, panel_space, gap_space):
        self.name = name
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.slope = get_distance(topRight, topLeft)
        self.columns = []
        self.slope = (topRight.y - bottomRight.y) / (topRight.x - bottomRight.x)

        # panel_space = 92
        # gap_space = 29
        i = 0
        dist = 0
        length = get_distance(topRight, bottomRight)
        while dist < length:
            breaks = int(i / 38)
            dist = (panel_space * i) + (gap_space * breaks) + (panel_space * .5)
            self.columns.append(next_coordinate_right(topRight, dist, self.slope))
            i += 1

        # print 'Rectangle: ' + self.name
        # print 'has a max columns of: ' + str(i)

        if i < 100:
            calc_gap = length

    def sum_of_distances(self, point):
        if not isinstance(point, Coordinate):
            raise ValueError('point passed in is not a coordinate')

        sum = get_distance(self.topLeft, point)
        sum += get_distance(self.topRight, point)
        # sum += get_distance(self.bottomLeft, point)
        # sum += get_distance(self.bottomRight, point)
        return sum


def get_rectangle(rectangles, point):
    if not isinstance(point, Coordinate):
        raise ValueError('point passed in is not a coordinate')

    min_rec = None

    for r in rectangles:
        if not isinstance(r, Rectangle):
            raise ValueError('rectangles were not passed in')
        # Can make faster by storing the sum of distance and not rerunning

        # print 'rect ' + r.name + ' sum = ' + str(r.sum_of_distances(point))
        # print 'topLeft = ' + str(get_distance(r.topLeft, point))
        # print 'topRight = ' + str(get_distance(r.topRight, point))
        # print 'bottomLeft = ' + str(get_distance(r.bottomLeft, point))
        # print 'bottomRight = ' + str(get_distance(r.bottomRight, point))
        # print ''

        if min_rec is None:
            min_rec = r
        elif min_rec.sum_of_distances(point) > r.sum_of_distances(point):
            min_rec = r

    return min_rec


def get_column(r, point):
    # find closest column first
    i = 1
    last_dist = get_distance(point, r.columns[0])
    curr_dist = get_distance(point, r.columns[i])
    while curr_dist < last_dist:
        last_dist = curr_dist
        i += 1
        try:
            curr_dist = get_distance(point, r.columns[i])
        except IndexError:
            print 'Error trying to get to ' + str(i)
            return -1

    # index ends 1 after the closest, but index starts at 0 and column # doesn't
    return i


def get_direction(r, point):
    north = get_distance(point, r.topRight) + get_distance(point, r.bottomRight)
    south = get_distance(point, r.topLeft) + get_distance(point, r.bottomLeft)
    #print 'rect ' + r.name + ' sum = ' + str(r.sum_of_distances(point))
    # print 'topLeft = ' + str(get_distance(r.topLeft, point))
    # print 'topRight = ' + str(get_distance(r.topRight, point))
    # print 'bottomLeft = ' + str(get_distance(r.bottomLeft, point))
    # print 'bottomRight = ' + str(get_distance(r.bottomRight, point))
    # print 'north = ' + str(north)
    # print 'south = ' + str(south)
    # print ''

    if north < south:
        return 'north'
    else:
        return 'south'


def get_column_law_of_cos(r, point):
    total_line = get_distance(r.topRight, r.bottomRight)
    # User larger triangle for better accuracy
    if get_distance(r.topRight, point) > get_distance(r.topLeft, point):
        hypotenuse_t = get_distance(r.topRight, point)
        hypotenuse_b = get_distance(r.bottomRight, point)
    else:
        print 'using non normal'
        hypotenuse_t = get_distance(r.topLeft, point)
        hypotenuse_b = get_distance(r.bottomLeft, point)

    print 'hypot_t = ' + str(hypotenuse_t)
    print 'hypot_b = ' + str(hypotenuse_b)

    loc_num = ((total_line ** 2) + (hypotenuse_b ** 2) - (hypotenuse_t ** 2))
    print 'loc_num = ' + str(loc_num)
    loc_den = (2 * hypotenuse_b * total_line)
    print 'loc_den = ' + str(loc_den)
    loc = loc_num / loc_den
    print 'loc = ' + str(loc)
    partial_line2 = loc * hypotenuse_t
    print 'partial line2 = ' + str(partial_line2)

    # law of cosines returns cos of t angle then trig formula (aka times it by the hypotenuse
    partial_line = (((total_line ** 2) + (hypotenuse_b ** 2) - (hypotenuse_t ** 2)) / (
        2 * hypotenuse_b * total_line)) * hypotenuse_t

    # for test
    print 'total line = ' + str(total_line)
    print 'partial line = ' + str(partial_line)

    opposite_line = (((total_line ** 2) + (hypotenuse_t ** 2) - (hypotenuse_b ** 2)) / (
        2 * hypotenuse_t * total_line)) * hypotenuse_b
    print 'opposite line = ' + str(opposite_line)
    print partial_line + opposite_line

    # 38 rows each 93 pixels long before a gapof 29 needs to be accounted for
    cSpace = (38 * 93)
    start2 = cSpace + 29
    start3 = cSpace + 29 + cSpace + 29
    if partial_line <= cSpace:
        return int(partial_line / 38)
    elif partial_line <= (start2 + cSpace):
        return int((partial_line - start2) / 38)
    elif partial_line <= (start3 + cSpace):
        return int((partial_line - start3) / 38)
