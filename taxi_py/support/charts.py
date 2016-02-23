from __future__ import division

import matplotlib.pyplot as plt
import numpy as np

_rgb = lambda r, g, b: (r / 255, g / 255, b / 255)

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    _rgb(220, 220, 220)  # gray
)

class two_pie_chart(object):
    def __init__(self, _labels, title1, per_data1, title2, per_data2):
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(121)
        labels = []
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data1[i]))
        ax.pie(per_data1, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title1)
        
        ax = fig.add_subplot(122)
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data2[i]))
        ax.pie(per_data2, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(title2)
        
        plt.show()
        

class bar_chart(object):
    def __init__(self, _title, _ylabel, xTickMarks, _data):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ind = np.arange(len(_data))
        width = 0.4  # the width of the bars
        #
        ax.bar(ind, _data, width, color='blue')
        # axes and labels
        ax.set_xlim(-width, len(ind) + width)
        ax.set_ylabel(_ylabel)
        ax.set_title(_title)
        ax.set_xticks(ind + width)
        xtickNames = ax.set_xticklabels(xTickMarks)
        plt.setp(xtickNames, rotation=25, fontsize=10)
        
        # # add a legend
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

class multiple_line_chart(object):
    def __init__(self, _title, _ylabel, x_data, multi_y_data, legend_labels):
        assert len(multi_y_data) == len(legend_labels) 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(_title)
        ax.set_ylabel(_ylabel)
        ymax = 0
        for i, y_data in enumerate(multi_y_data):
            plt.plot(x_data, y_data, linewidth=1, color=clists[i])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1 
        plt.legend(legend_labels, ncol=1, loc='upper left', fontsize=10)
        
        ax.set_xbound(lower=0-0.5, upper=len(multi_y_data[0]))
        ax.set_ybound(upper=ymax * 1.05)
        
        plt.show()

def test():
    labels = ['PInAP | DInAP', 'POutAP | DInAP']
    data_2009 = [0.2483495724173474, 0.75165042758265266]
    data_2010 = [0.30647775676350764, 0.69352224323649236]
    two_pie_chart(labels, "Drivers' decision in 2009", data_2009, "Drivers' decision in 2010", data_2010)
    
    
if __name__ == '__main__':
    test()