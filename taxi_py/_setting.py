from __future__ import division
#
import platform, sys

plf = platform.platform()

if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi'
#     sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
    sys.path.append('/home/ckhan/local/lib/python2.6/site-packages')
    #
    path_to_ori_data = '/home/taxi'
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi'
    path_to_ori_data = '.'
else:
    #TODO
    assert False, 'Windows?'
assert prefix

tm_dir = prefix+'/trips_merged'
dt_dir = prefix+'/drivers_trips'
dl_dir = prefix+'/drivers_logs'
ds_dir = prefix+'/drivers_shifts'