from __future__ import division
#
from shapely.geometry import Polygon, Point

ap_poly_info = 'airport_polygons'

class terminal_poly(Polygon):
    def __init__(self, tid, points):
        Polygon.__init__(self, points)
        self.tid = tid
    def __repr__(self):
        return self.tid

# generate a airport's polygon and terminal polygones
ap_poly = None
term_polys = []
with open(ap_poly_info, 'r') as f:
    ls = [w.strip() for w in f.readlines()]
for l in ls:
    t, p = l.split('=')
    points = []
    for location in p[len('POLYGON(('):-len('))')].split(','):
        _long, _lat = location.split(' ')
        points.append([eval(_long), eval(_lat)])
    if t == 'Airport':
        ap_poly = Polygon(points)
    else:
        tn = eval(t.split('-')[1])
        term_polys.append(terminal_poly(tn, points))

def check_terminal_num(_long, _lat):
    '''
    tn: the terminal number
       if the location is not in polygons it will return -1
    '''
    p = Point(_long, _lat)
    tn = -1
    for poly in term_polys:
        if p.within(poly):
            tn = poly.tid
            break
    del p
    return tn
    
def is_in_airport(_long, _lat):
    '''
    if the location in airport's polygon, return O
    otherwise, return X 
    '''
    p = Point(_long, _lat)
    rv = 'O' if p.within(ap_poly) else 'X'
    del p
    return rv