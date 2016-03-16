
# coding: utf-8

# In[1]:

from __future__ import division
#
import os, sys
sys.path.append(os.getcwd()+'/..')
#
import pandas as pd
#
from supports._setting import aiport_trips_dir
from supports.charts import multiple_line_chart
# get_ipython().magic(u'pylab inline')


# In[2]:

Y09 = pd.read_csv('%s/%s'%(aiport_trips_dir, 'Y09-airport-trip.csv'))
Y10 = pd.read_csv('%s/%s'%(aiport_trips_dir, 'Y10-airport-trip.csv'))


# In[3]:

SEC = 60
Y09_hourly_gb, Y10_hourly_gb = Y09.groupby(['hh']), Y10.groupby(['hh'])
Y09_hourly_qt = [ x / SEC for x in Y09_hourly_gb.mean()['queue-time']]
Y10_hourly_qt = [ x / SEC for x in Y10_hourly_gb.mean()['queue-time']]


# In[4]:

multiple_line_chart('Hourly queue time', 'Times', 'Minutes', range(24), [Y09_hourly_qt, Y10_hourly_qt], ['Y2009', 'Y2010'], 'upper right')


# In[ ]:



