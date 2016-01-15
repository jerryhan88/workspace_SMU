from __future__ import division
#
import platform, os
import csv
#
from shapely.geometry import Polygon, Point
#
plf = platform.platform()

trips_folder = None
if plf.startswith('Linux'):
    # This would be the server
    trips_folder = '/home/ckhan/taxi/trips'
    driver_folder = '/home/ckhan/taxi/trips/drivers'
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    trips_folder = '/Users/JerryHan88/taxi/trips'
    driver_folder = '/Users/JerryHan88/taxi/trips/drivers'
else:
    assert False, 'Windows?'

_poly_info = 'airport_polygons'
term_polys = None

def write_trip_on_driver(driver_id):
    pass

def run():
    global term_polys
    term_polys = gen_terminal_polygons()
    if not os.path.exists(driver_folder): os.makedirs(driver_folder)
    for fn in os.listdir(trips_folder):
        if not fn.endswith('.csv'): continue
        with open('%s/%s' % (trips_folder, fn), 'rb') as csvfile:
            reader = csv.reader(csvfile)
            headers = reader.next()
            index_did = headers.index('driver-id')
            for row in reader:
                print row
                driver_id = row[index_did]
                write_driver_trip(headers, driver_id, row)

def write_driver_trip(headers, driver_id, row):
    '''
    Also check where this trip is started and ended
    '''
    fn = '%s/driver-%s-trips.csv' % (driver_folder, driver_id)
    index_s_long, index_s_lat = headers.index('start-long'), headers.index('start-lat')
    index_e_long, index_e_lat = headers.index('end-long'), headers.index('end-lat')   
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvfile:
            writer = csv.writer(csvfile)
            new_headers = headers + ['start-terminal', 'end-terminal']
            writer.writerow(new_headers)
    #
    s_long, s_lat = eval(row[index_s_long]), eval(row[index_s_lat])
    e_long, e_lat = eval(row[index_e_long]), eval(row[index_e_lat]) 
    new_row = row + [check_in_airport(s_long, s_lat), check_in_airport(e_long, e_lat)]
    with open(fn, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)

def check_in_airport(_long, _lat):
    global term_polys
    p = Point(_long, _lat)
    tn = -1
    for poly in term_polys:
        if p.within(poly):
            tn = poly.tid
            break
    del p
    return tn

def gen_terminal_polygons():
    polygons = []
    with open(_poly_info, 'r') as f:
        ls = [w.strip() for w in f.readlines()]
    for l in ls:
        t, p = l.split('=')
        if t == 'Airport':
            continue
        tn = eval(t.split('-')[1])
        points = []
        for location in p[len('POLYGON(('):-len('))')].split(','):
            long, lat = location.split(' ')
            points.append([eval(long), eval(lat)]) 
        polygons.append(terminal_poly(tn, points))
    return polygons

class terminal_poly(Polygon):
    def __init__(self, tid, points):
        Polygon.__init__(self, points)
        self.tid = tid
    def __repr__(self):
        return self.tid
        

if __name__ == '__main__':
    run()
