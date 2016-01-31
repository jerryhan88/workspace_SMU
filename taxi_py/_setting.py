from __future__ import division
#
import platform, sys

plf = platform.platform()

if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi'
    py_vinfo = sys.version_info
    if py_vinfo.major == 2 and py_vinfo.minor == 7:
        sys.path.append('/home/ckhan/local/lib/python2.7/site-packages')
        sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
    else:
        print 'This python is not 2.7 version'
        assert False
    
#     sys.path.append('/home/ckhan/local/lib/python2.6/site-packages')
    #
    path_to_ori_data = '/home/taxi'
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi'
    path_to_ori_data = '/Users/JerryHan88/taxi'
else:
    #TODO
    assert False, 'Windows?'
assert prefix

tm_dir = prefix+'/trips_merged'
dt_dir = prefix+'/drivers_trips'
dl_dir = prefix+'/drivers_logs'
ds_dir = prefix+'/drivers_shifts'
l_dir = prefix+'/logs_ext'
t_dir = prefix+'/trips_ext'
s_dir = prefix+ '/shifts'
q_dir = prefix+ '/queue_data'