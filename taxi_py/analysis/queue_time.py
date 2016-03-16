
# coding: utf-8

# In[46]:

from __future__ import division
#
import os, sys
sys.path.append(os.getcwd()+'/..')
#
import pandas as pd
#
from supports._setting import aiport_trips_dir
from supports.charts import histograms
#%pylab inline
#pylab.rcParams['figure.figsize'] = (20, 10)


# In[47]:

df_Y2009 = pd.read_csv('%s/%s'%(aiport_trips_dir, 'airport-trip-09.csv'))
df_Y2010 = pd.read_csv('%s/%s'%(aiport_trips_dir, 'airport-trip-10.csv'))


# In[48]:

queue_time_Y2009, queue_time_Y2010 = list(df_Y2009['queue-time']), list(df_Y2010['queue-time'])
chart_info = [
    [('Y2009', 'Queue time', 'Probability', 50, queue_time_Y2009), 
     ('Y2010', 'Queue time', 'Probability', 50, queue_time_Y2010)
    ]
]
histograms(chart_info)


# In[49]:

filtered_df_Y2009 = df_Y2009[(0 < df_Y2009['queue-time']) & (df_Y2009['queue-time'] < 7200)]
filtered_df_Y2010 = df_Y2010[(0 < df_Y2010['queue-time']) & (df_Y2010['queue-time'] < 7200)]


# In[50]:

queue_time_Y2009, queue_time_Y2010 = list(filtered_df_Y2009['queue-time']), list(filtered_df_Y2010['queue-time'])
chart_info = [
    [('Y2009', 'Queue time', 'Probability', 30, queue_time_Y2009), 
     ('Y2010', 'Queue time', 'Probability', 30, queue_time_Y2010)
    ]
]
histograms(chart_info)


# In[ ]:



