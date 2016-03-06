def process_file(path_to_csv_file):
    ori_log_fn = path_to_csv_file.split('/')[-1]
    _, yymm, _ = ori_log_fn.split('-')
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm )
    vehicle_ap_crossing_time_from_out_to_in = {}
    vehicle_current_ap_or_not = {}
    with open(path_to_csv_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_time, id_vid, id_did = headers.index('time'), headers.index('vehicle-id'), headers.index('driver-id')
        index_long, index_lat = headers.index('longitude'), headers.index('latitude')
        for row in reader:        
            ap_or_not = is_in_airport(eval(row[index_long]), eval(row[index_lat]))
            t = eval(row[id_time])
            vid = row[id_vid]
            vehicle_current_ap_or_not.setdefault(vid, )
            
            if True:
                crossing_time = None
                vehicle_ap_crossing_time_from_out_to_in.setdefault(vid, [t]).append(crossing_time)