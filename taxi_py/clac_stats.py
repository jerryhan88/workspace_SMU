from __future__ import division
#
import pandas as pd
import csv
#
from _setting import l_dir, t_dir, s_dir
from logger import logging_msg
#
def run():
    
    jobs_counter = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            whole_procedure('%02d%02d' % (y, m))
            jobs_counter += 1
            break
    pass

def calc_duration(s_df, did):
    whole_working_time, time_for_ap = None, None
    
    
    
    return whole_working_time, time_for_ap
    
    
    
    
    

def whole_procedure(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    
    yy, mm = int(yymm[:2]), int(yymm[2:])
    if mm == 1:
        if yy == 9:
            prev_month = None
        else:
            prev_month = '0912'
    else:
        prev_month = '%02d%02d' % (yy, mm - 1)
#     pl_df = pd.read_csv('%s/logs-%s-normal.csv' % (l_dir, prev_month)) if prev_month else None        
#     cl_df = pd.read_csv('%s/logs-%s-normal.csv' % (l_dir, yymm))
    t_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, yymm))
    
    did_l = 'driver-id'
    tm_l = 'trip-mode'
    
    t_df.loc[(t_df[tm_l] == 3)].groupby(did_l).sum()[]
    t_df
    


#     s_df = pd.read_csv('%s/shift-%s.csv' % (s_dir, yymm))

#     duration_l = 'duration'
#     print s_df.groupby(did_l).sum()[duration_l].loc[4]
    
    
# 1        19627
# 2        14493
# 4        25237
# 6         1710
# 7        18680
# 8        13172
# 10       36420
# 11       11523
    assert False
    
    t_csv = '%s/logs-%s-normal.csv' % (t_dir, yymm)
    
    with open(t_csv, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        
        
        id_did = headers.index(did_l)
        for row in reader:
            did = row[id_did]
            # calculate whole working time
            s_df.loc[(s_df[did_l] == did, [duration_l])].sum
            
            #     print df.loc[(df['start-time'] <= 1232405340), ['fare', 'driver-id']]
            
            
            assert False
        
        
        
        assert False
#         new_header = ['']
#         'trip-id'
#         'driver-id'
#         'vehicle-id'
#         'trip-mode'
#         'fare'
#             start-terminal    end-terminal    
#         
#         logging-time
#         ap-or-not
#         
#         
#         start-time    end-time
        
        
        id_s_time, id_e_time = headers.index('start-time'), headers.index('end-time')
        id_s_long, id_s_lat = headers.index('start-long'), headers.index('start-lat')
        id_e_long, id_e_lat = headers.index('end-long'), headers.index('end-lat')
        driver_prev_lacation = {}
        indexes = [id_driver_id, id_s_time, id_e_time, id_s_long, id_s_lat, id_e_long, id_e_lat]
        pt_new_csv = '%s/%s' % (t_dir, pt_log_csv.split('/')[-1])
        with open(pt_new_csv, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
    
    pass


if __name__ == '__main__':
    run()
