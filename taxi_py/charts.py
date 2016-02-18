from __future__ import division

import matplotlib.pyplot as plt
import numpy as np

class two_pie_chart(object):
    def __init__(self, _labels, title1, per_data1, title2, per_data2):
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(121)
        labels = []
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f %%)' % (l, per_data1[i]))
        explode = (0.05, 0.05, 0.05, 0)
        ax.pie(per_data1, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title1)
        
        ax = fig.add_subplot(122)
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f %%)' % (l, per_data2[i]))
        explode = (0.05, 0.05, 0.05, 0)
        ax.pie(per_data2, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title2)
        
        plt.show()
        
class one_bar_chart(object):
    def __init__(self, _title, _ylabel, xTickMarks, data1, data2, legends):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #
        ind = np.arange(len(data1))
        width = 0.4  # the width of the bars
        
        # # the bars
        rects1 = ax.bar(ind, data1, width, color='blue')
        rects2 = ax.bar(ind + width, data2, width, color='red')
        
        # axes and labels
        ax.set_xlim(-width, len(ind) + width)
        ax.set_ylabel(_ylabel)
        ax.set_title(_title)
        ax.set_xticks(ind + width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=25, fontsize=10)
        
        # # add a legend
        ax.legend((rects1[0], rects2[0]), legends)
        plt.show()
    