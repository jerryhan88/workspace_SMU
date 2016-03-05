from __future__ import division
import os, sys, csv
sys.path.append(os.getcwd() + '/..')
#
from support._setting import ms_dir
from support.handling_pkl import save_pickle_file

def run():
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            process_file(yymm)
    
def process_file(yymm):
    full_vid_did = set()
    with open('%s/shift-hour-state-%s.csv' % (ms_dir, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id')
        for row in reader:
            vid, did = row[id_vid], row[id_did]
            full_vid_did.add((vid, did))
    pkl_fn = 'full-vid-did-%s.pkl' % yymm
    save_pickle_file('%s/%s' % (ms_dir, pkl_fn), full_vid_did) 

if __name__ == '__main__':
    run()
