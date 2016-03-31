from __future__ import division
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.path import Path
import matplotlib.patches as patches

_rgb = lambda r, g, b: (r / 255, g / 255, b / 255)

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    _rgb(220, 220, 220)  # gray
)

class histogram(object):
    def __init__(self, _title, x_label, y_label, num_bin, x_data):
        plt.figure(figsize=(6, 6))
        _, bins, _ = plt.hist(x_data, 50, normed=1, facecolor='green', alpha=0.75)
        x_mean, x_std = np.mean(x_data), np.std(x_data)
        # add a 'best fit' line
        plt.plot(bins, mlab.normpdf(bins, x_mean, x_std), 'r--', linewidth=1)
        #
        plt.xlabel(x_label); plt.ylabel(y_label)
        plt.title(r'$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_title, x_mean, x_std))
        plt.show()

class histograms(object):
    def __init__(self, chart_info):
        # chart_info is two dimensional array (list)
        # The first dimension means rows
        # ex. 2X2 charts
        # [
        # [(_title, x_label, y_label, num_bin, x_data), (_title, x_label, y_label, num_bin, x_data)],
        # [(_title, x_label, y_label, num_bin, x_data), (_title, x_label, y_label, num_bin, x_data)]
        # ] 
        plt.figure(figsize=(12, 6))
        _, axarr = plt.subplots(len(chart_info), len(chart_info[0]))
        for i, row in enumerate(chart_info):
            for j, (_title, x_label, y_label, num_bin, x_data) in enumerate(row):
                ax = axarr[i + j]
                _, bins, _ = ax.hist(x_data, num_bin, normed=1, facecolor='green', alpha=0.75)
                x_mean, x_std = np.mean(x_data), np.std(x_data)
                # add a 'best fit' line
                ax.plot(bins, mlab.normpdf(bins, x_mean, x_std), 'r--', linewidth=1)
                #
                ax.set_xlabel(x_label); ax.set_ylabel(y_label)
                ax.set_title(r'$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_title, x_mean, x_std))
        plt.show()

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
    def __init__(self, _title, _xlabel, _ylabel, x_data, multi_y_data, legend_labels, legend_pos, _xticks=[]):
        assert len(multi_y_data) == len(legend_labels)
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        ax.set_title(_title)
        ax.set_xlabel(_xlabel)
        ax.set_ylabel(_ylabel)
        ymax = 0
        for i, y_data in enumerate(multi_y_data):
            plt.plot(x_data, y_data, linewidth=1, color=clists[i])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1 
        
#         xtickNames = ax.set_xticklabels(_xticks)
        plt.xticks(x_data, _xticks, rotation=30)
        
#         xtickNames = plt.xticks(x_data, _xticks)
#         plt.setp(xtickNames, rotation=25, fontsize=10)
        plt.legend(legend_labels, ncol=1, loc=legend_pos, fontsize=10)
        ax.set_xbound(lower=0, upper=x_data[-1])
        ax.set_ybound(upper=ymax * 1.05)
        
        plt.show()

class bar_table(object):
    def __init__(self, _title, _ylabel, row_labels, col_labels, table_data):
        assert len(table_data) == len(row_labels)
        assert len(table_data[0]) == len(col_labels)
        #
        index, bar_width = np.arange(len(col_labels)) + 0.3, 0.4
        #
        bar_data = table_data[:]
        bar_data.reverse()
        y_offset = np.array([0.0] * len(col_labels))
        for i, row_data in enumerate(bar_data):
            plt.bar(index, row_data, bar_width, bottom=y_offset, color=clists[i])
            y_offset = y_offset + row_data
#         cell_text.reverse()
#         row_labels.reverse()
        #
        table = plt.table(cellText=table_data, colLabels=col_labels, rowLabels=row_labels, loc='bottom')
        table.scale(1, 2)
        #
        plt.subplots_adjust(left=0.2, bottom=0.2)
        plt.ylabel(_ylabel)
        plt.xticks([])
        plt.title(_title)
        plt.show()

class grid_charts(object):
    UNIT = 1.0
    HALF_UNIT = UNIT / 2
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    FIG_SIZE_UNIT = 6
    def __init__(self, x_axis_info, y_axis_info, _legends, titles, _data, fn=None):
        _xlabel, _xticks = x_axis_info
        _ylabel, _yticks = y_axis_info
        num_charts = len(_data)
        #
        fig = plt.figure(figsize=(grid_charts.FIG_SIZE_UNIT * num_charts, grid_charts.FIG_SIZE_UNIT))
        
        if fn:
            # TODO save it !!
            for i, points_color in enumerate(_data):
                self.draw_a_chart(fig, num_charts, i, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color)
            plt.savefig(fn)
        else:
            for i, points_color in enumerate(_data):
                self.draw_a_chart(fig, num_charts, i, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color, titles[i])
        plt.show()
        
    def draw_a_chart(self, fig, num_charts, _th, _legends, _xlabel, _ylabel, _xticks, _yticks, points_color, title=None):
        paths, color_choices = [], []
        for x, y, c in points_color:
            verts = self.gen_rect_coord_by_center(x, y)
            paths.append(Path(verts, grid_charts.codes))
            color_choices.append(c)
        colors_set = set(color_choices)
        labeled = [False for _ in xrange(len(colors_set))]
        ax = fig.add_subplot(1, num_charts, _th + 1)
        for i, path in enumerate(paths):
            if not labeled[color_choices[i]]:
                patch = patches.PathPatch(path, facecolor=clists[color_choices[i]], label='%s' % _legends[color_choices[i]])
                labeled[color_choices[i]] = True
            else:
                patch = patches.PathPatch(path, facecolor=clists[color_choices[i]])
            ax.add_patch(patch)
        xs, ys, _ = zip(*points_color)
        ax.set_xlim(min(xs) - grid_charts.HALF_UNIT, max(xs) + grid_charts.HALF_UNIT)
        ax.set_ylim(min(ys) - grid_charts.HALF_UNIT, max(ys) + grid_charts.HALF_UNIT)
        #
        if title: plt.text(0.5, 1.08, title, horizontalalignment='center', transform = ax.transAxes)
        if _xlabel: plt.xlabel(_xlabel)
        if _ylabel: plt.ylabel(_ylabel)
        if _xticks: plt.xticks(_xticks)
        if _yticks: plt.yticks(range(len(_yticks)), _yticks)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0., framealpha=0.0)
        
                
    def gen_rect_coord_by_center(self, x, y):
        left_bottom = (x - grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT) 
        left_top = (x - grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_top = (x + grid_charts.HALF_UNIT, y + grid_charts.HALF_UNIT)
        right_bottom = (x + grid_charts.HALF_UNIT, y - grid_charts.HALF_UNIT)
        ignored = left_bottom
        return [left_bottom, left_top  , right_top , right_bottom, ignored]

def test():
#     _xticks = ['0901', '0902', '0903', '0904', '0905', '0906', '0907', '0908', '0909', '0910', '0911', '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1011', '1012'] 
#     multi_y_data = [[0.67635201228038688, 0.701050888316745, 0.66084240390978122, 0.65022445963619491, 0.64389675477843911, 0.66446136896636077, 0.63970548026605123, 0.66264901079546956, 0.71122657414666435, 0.68196171545278039, 0.66778103715483994, 0.66645472088965307, 0.77031418724961354, 0.70967712712012176, 0.72621150500366061, 0.70573424978336496, 0.72104493110684764, 0.71686910585881769, 0.73506509548629695, 0.74608701714712922, 0.72765325055878005, 0.69799623445198877], [0.62281952926979178, 0.64994921475140077, 0.64245864641897543, 0.62093270275139034, 0.60998069599320515, 0.63685663554035121, 0.59950742051005435, 0.62807663503311439, 0.67665595563848002, 0.65691655100276258, 0.63350297404335509, 0.63354886905649876, 0.73769631165216809, 0.69010429756449398, 0.69883330776666552, 0.6750773528391254, 0.71623210955924899, 0.70178444283012997, 0.7103634031797581, 0.72451101298465392, 0.71816134205083848, 0.68908767880702615]]
#     
#     multiple_line_chart('_title', '_xlabel', '_ylabel', range(len(_xticks)), multi_y_data, ['prev_in','prev_out'], 'upper left', _xticks) 
#     
    _data = [[834039, 1207006], [2520670, 2730197]]
    row_labels, col_labels = ['Pick up in AP', 'Pick up out AP'], ['# of trips in Y2009', '# of trips in Y2010']
    
    bar_table('Airport trips', 'Number of trips', row_labels, col_labels, _data)
    
if __name__ == '__main__':
    test()
