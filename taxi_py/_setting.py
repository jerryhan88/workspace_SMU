from __future__ import division
#
import platform, sys

plf = platform.platform()
 
if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi'
    sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi'
else:
    #TODO
    assert False, 'Windows?'
assert prefix

tm_dir = prefix+'/trips_merged'
dt_dir = prefix+'/drivers_trips'

ap_poly_info = 'airport_polygons'