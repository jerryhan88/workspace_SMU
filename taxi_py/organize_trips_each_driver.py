from __future__ import division
#
import os, shutil, csv
#
from _setting import tm_dir, dt_dir, ap_poly_info
#
from shapely.geometry import Polygon, Point
 

driver_prev_lacation_time = {}
BREAK_LIMIT = 60 * 60 * 12 # To consider long time break such as shift or logoff
#
def run():
    cvs_files = [fn for fn in os.listdir(tm_dir) if fn.endswith('.csv')]
    # generate terminal polygones
    term_polys = []
    with open(ap_poly_info, 'r') as f:
        ls = [w.strip() for w in f.readlines()]
    for l in ls:
        t, p = l.split('=')
        if t == 'Airport':
            continue
        tn = eval(t.split('-')[1])
        points = []
        for location in p[len('POLYGON(('):-len('))')].split(','):
            _long, _lat = location.split(' ')
            points.append([eval(_long), eval(_lat)]) 
        term_polys.append(terminal_poly(tn, points))
    #
    if os.path.exists(dt_dir):
        shutil.rmtree(dt_dir)
        os.makedirs(dt_dir)
    for fn in sorted(cvs_files):
        print 'start', fn
        with open('%s/%s' % (tm_dir, fn), 'rb') as csvfile:
            reader = csv.reader(csvfile)
            headers = reader.next()
            index_did = headers.index('driver-id')
            for row in reader:
                driver_id = row[index_did]
                write_driver_trip(headers, driver_id, row, term_polys)
        print 'end', fn

def write_driver_trip(headers, driver_id, row, term_polys):
    '''
    Also check where this trip is started and ended
    '''
    def check_in_airport(_long, _lat):
        p = Point(_long, _lat)
        tn = -1
        for poly in term_polys:
            if p.within(poly):
                tn = poly.tid
                break
        del p
        return tn
    
    index_s_time, index_e_time = headers.index('start-time'), headers.index('end-time')
    index_s_long, index_s_lat = headers.index('start-long'), headers.index('start-lat')
    index_e_long, index_e_lat = headers.index('end-long'), headers.index('end-lat')   
    
    fn = '%s/driver_%s_trips.csv' % (dt_dir, driver_id)
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvfile:
            writer = csv.writer(csvfile)
            new_headers = headers + ['start-terminal', 'end-terminal', 'trip-mode']
            writer.writerow(new_headers)
    #
    s_long, s_lat = eval(row[index_s_long]), eval(row[index_s_lat])
    e_long, e_lat = eval(row[index_e_long]), eval(row[index_e_lat])
    c_s_ter, c_e_ter = check_in_airport(s_long, s_lat), check_in_airport(e_long, e_lat)
    '''
    Set a trip mode
    Trips for servicing passengers are classified according to positions 
      where the driver dropped the previous passenger off and picks the current passenger up. 
    Positions are categorised as in the airport (InAP) or outside of airport (OutAP). 
    As a result, four trip modes can be derived;
        - drop off InAP - pick up InAP             -> 0
        - drop off InAP - pick up OutAP            -> 1
        - drop off OutAP - pick up InAP            -> 2
        - drop off OutAP - pick up OutAP           -> 3
    Also, one more mode is added to represent trip of which previous trip was handled more than 12 hours ago.
        - previous trip occured 12 hours before    -> -1
    '''
    if not driver_prev_lacation_time.has_key(driver_id):
        driver_prev_lacation_time[driver_id] = (c_e_ter, eval(row[index_e_time])) 
        trip_mode = -1
    else:
        p_e_ter, p_e_time = driver_prev_lacation_time[driver_id]
        c_s_time = eval(row[index_s_time]) 
        if c_s_time - p_e_time > BREAK_LIMIT:
            trip_mode = -1
        elif p_e_ter != -1 and c_s_ter != -1 :
            trip_mode = 0
        elif p_e_ter != -1 and c_s_ter == -1:
            trip_mode = 1
        elif p_e_ter == -1 and c_s_ter != -1:
            trip_mode = 2
        elif p_e_ter == -1 and c_s_ter == -1:
            trip_mode = 3
        else:
            assert False
    new_row = row + [check_in_airport(s_long, s_lat), check_in_airport(e_long, e_lat), trip_mode]
    with open(fn, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)

class terminal_poly(Polygon):
    def __init__(self, tid, points):
        Polygon.__init__(self, points)
        self.tid = tid
    def __repr__(self):
        return self.tid
        

if __name__ == '__main__':
    run()
