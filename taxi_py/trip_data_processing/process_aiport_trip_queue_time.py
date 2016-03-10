from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
from bisect import bisect
#
from supports._setting import aiport_trips_dir, trips_dir, logs_dir
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports.handling_pkl import load_picle_file
from supports.etc_functions import get_all_files
from supports.logger import logging_msg

def run():
#     remove_creat_dir(aiport_trips_dir)
    csv_files = get_all_files(trips_dir, 'whole-trip-', '.csv')
    for fn in csv_files:
        process_file(fn)
        
def process_file(fn):
    _, _, yymm = fn[:-len('.csv')].split('-')
    if os.path.exists('%s/airport-trip-%s.csv' % (aiport_trips_dir, yymm)):
        return None
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm)
    
    pkl_files = get_all_files(logs_dir, 'crossing-time-', '.pkl')
    pkl_file_path = None
    for pkl_fn in pkl_files:
        _, _, pkl_yymm = pkl_fn[:-len('.pkl')].split('-')
        if pkl_yymm == yymm:
            pkl_file_path = '%s/%s' % (logs_dir, pkl_fn)
            break
    else:
        assert False, yymm
    whole_crossing_times = load_picle_file(pkl_file_path)
    #
    with open('%s/%s' % (trips_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_tid, id_vid, id_did = headers.index('tid'), headers.index('vid'), headers.index('did')
        id_st, id_et, id_duration = headers.index('start-time'), headers.index('end-time'), headers.index('duration') 
        id_fare, id_tm, id_prev_tet = headers.index('fare'), headers.index('trip-mode'), headers.index('prev-trip-end-time')
        #
        with open('%s/airport-trip-%s.csv' % (aiport_trips_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did',
                           'start-time', 'end-time', 'duration',
                           'fare', 'trip-mode', 'prev-trip-end-time',
                           'join-queue-time', 'queue-time']
            writer.writerow(new_headers)
            for row in reader:
                tm = int(row[id_tm])
                if tm == DInAP_POutAP or tm == DOutAP_POutAP:
                    continue
                vid, st, prev_tet = row[id_vid], eval(row[id_st]), eval(row[id_prev_tet])
                if tm == DInAP_PInAP:
                    join_queue_time = prev_tet 
                else:
                    assert tm == DOutAP_PInAP
                    try:
                        i = bisect(whole_crossing_times[vid], st)
                    except KeyError:
                        logging_msg('%s-tid-%s' % (yymm, row[id_tid]))
                        continue
                    join_queue_time = whole_crossing_times[vid][i - 1] if i != 0 else whole_crossing_times[vid][0]
                queue_time = st - join_queue_time
                new_row = [row[id_tid], vid, row[id_did],
                            st, row[id_et], row[id_duration],
                            row[id_fare], tm, prev_tet,
                            join_queue_time, queue_time ]
                writer.writerow(new_row)
    print 'end the file; %s' % yymm 
    logging_msg('end the file; %s' % yymm)
         
if __name__ == '__main__':
    run()
