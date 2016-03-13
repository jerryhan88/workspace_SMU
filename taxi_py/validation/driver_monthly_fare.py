
# coding: utf-8

# In[1]:

from __future__ import division
#
import os, sys
sys.path.append(os.getcwd()+'/..')
#
import pandas as pd
#
from supports._setting import trips_dir, aiport_trips_dir
from supports.charts import histograms


# In[2]:

trip_prefix, ap_trip_prefix = 'whole-trip-', 'airport-trip-'


# In[3]:

Y09_driver_total_monthly_fare, Y10_driver_total_monthly_fare= [], []
Y09_driver_ap_monthly_fare, Y10_driver_ap_monthly_fare = [], []


# In[4]:

for m in xrange(1, 13):
    yymm = '09%02d' % (m) 
    if yymm in ['0912', '1010']:
        continue
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    trip_df = trip_df[(trip_df['did'] != -1)]
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (aiport_trips_dir, ap_trip_prefix, yymm))
    ap_trip_df = ap_trip_df[(ap_trip_df['did'] != -1)]

    Y09_driver_total_monthly_fare += list(trip_df.groupby(['did']).sum()['fare'])
    Y09_driver_ap_monthly_fare += list(ap_trip_df.groupby(['did']).sum()['fare'])


# In[6]:

Y10_driver_ap_monthly_fare = []
for m in xrange(1, 13):
    yymm = '10%02d' % (m) 
    if yymm in ['0912', '1010']:
        continue
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    trip_df = trip_df[(trip_df['did'] != -1)]
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (aiport_trips_dir, ap_trip_prefix, yymm))
    ap_trip_df = ap_trip_df[(ap_trip_df['did'] != -1)]

    Y10_driver_total_monthly_fare += list(trip_df.groupby(['did']).sum()['fare'])
    Y10_driver_ap_monthly_fare += list(ap_trip_df.groupby(['did']).sum()['fare'])


# In[11]:

chart_info = [
    [('Y2009', 'Fare (S$)', 'Probability', 50, [x / 100 for x in Y09_driver_total_monthly_fare]), 
     ('Y2010', 'Fare (S$)', 'Probability', 50, [x / 100 for x in Y10_driver_total_monthly_fare])
    ]
]
histograms(chart_info)


# In[10]:

chart_info = [
    [('Y2009', 'Fare (S$)', 'Probability', 25, [x / 100 for x in Y09_driver_ap_monthly_fare]), 
     ('Y2010', 'Fare (S$)', 'Probability', 25, [x / 100 for x in Y10_driver_ap_monthly_fare])
    ]
]
histograms(chart_info)


# In[ ]:



