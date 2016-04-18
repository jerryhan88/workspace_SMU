from __future__ import division
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.path import Path
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D

_rgb = lambda r, g, b: (r / 255, g / 255, b / 255)

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    _rgb(220, 220, 220),  # gray
    'yellow'
)

mlists = (
'o', #    circle
'v', #    triangle_down
'^', #    triangle_up
'<', #    triangle_left
'>', #    triangle_right
's', #    square
'p', #    pentagon
'*', #    star
'+', #    plus
'x', #    x
'D', #    diamond
'h', #    hexagon1
'1', #    tri_down
'2', #    tri_up
'3', #    tri_left
'4', #    tri_right
'8', #    octagon
'H', #    hexagon2
'd', #    thin_diamond
'|', #    vline
'_', #    hline
'.', #    point
',', #    pixel
          )

save_dir = '/Users/JerryHan88/Desktop/'

class one_histogram(object):
    def __init__(self, _title, x_label, y_label, num_bin, x_data, save_fn=None):
        plt.figure(figsize=(6, 6))
        _, bins, _ = plt.hist(x_data, num_bin, normed=1, facecolor='green', alpha=0.75)
        x_mean, x_std = np.mean(x_data), np.std(x_data)
        # add a 'best fit' line
        plt.plot(bins, mlab.normpdf(bins, x_mean, x_std), 'r--', linewidth=1)
        #
        plt.xlabel(x_label); plt.ylabel(y_label)
        plt.title(r'$\mathrm{%s}\ \mu=%.2f,\ \sigma=%.2f$' % (_title, x_mean, x_std))
        if save_fn:
            plt.savefig('%s/%s.pdf' % (save_dir, save_fn))
        plt.show()

class multiple_line_chart(object):
    def __init__(self, _figsize, _title, _xlabel, _ylabel, xticks_info, multi_y_data, y_legend_labels, legend_pos, save_fn=None):
        assert len(multi_y_data) == len(y_legend_labels)
        fig = plt.figure(figsize=_figsize)
        ax = fig.add_subplot(111)
        ax.set_title(_title)
        ax.set_xlabel(_xlabel)
        ax.set_ylabel(_ylabel)
        ymax = 0
        for i, y_data in enumerate(multi_y_data):
            plt.plot(range(len(y_data)), y_data, linewidth=1, color=clists[i], marker=mlists[i])
            ymax1 = max(y_data)
            if ymax < ymax1:
                ymax = ymax1
        ax.set_ybound(upper=ymax * 1.05)
        plt.legend(y_legend_labels, ncol=1, loc=legend_pos, fontsize=10)
        #
        _xticks, _rotation = xticks_info 
        plt.xticks(range(len(_xticks)), _xticks, rotation=_rotation)
        ax.set_xbound(lower=0, upper=range(len(_xticks))[-1])
        if save_fn:
            plt.savefig('%s/%s.pdf' % (save_dir, save_fn))
        plt.show()

class line_3D(object):
    def __init__(self, _figsize, _title, _xlabel, _ylabel, _zlabel, _data):
        fig = plt.figure(figsize=_figsize)
        ax = fig.gca(projection='3d')
        ax.set_title(_title); ax.set_xlabel(_xlabel); ax.set_ylabel(_ylabel); ax.set_zlabel(_zlabel)
        
        for xyz in _data:
            x, y, z = zip(*xyz)
            ax.plot(x, y, z)
            ax.legend()
        
#         theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
#         z = np.linspace(-2, 2, 100)
#         r = z ** 2 + 1
#         x = r * np.sin(theta)
#         y = r * np.cos(theta)
#         ax.plot(x, y, z, label='parametric curve')
        
        
        plt.show()


class bar_table(object):
    def __init__(self, _title, _ylabel, row_labels, col_labels, table_data, save_fn=None):
        assert len(table_data) == len(row_labels)
        assert len(table_data[0]) == len(col_labels)
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        #
        bar_width = 0.5
        ind = [bar_width / 2 + i for i in xrange(len(col_labels))]
#         index,  = np.arange(len(col_labels)), 
        #
        bar_data = table_data[:]
        bar_data.reverse()
        y_offset = np.array([0.0] * len(col_labels))
        for i, row_data in enumerate(bar_data):
            plt.bar(ind, row_data, bar_width, bottom=y_offset, color=clists[i])
            y_offset = y_offset + row_data
        ax.set_xlim(0, len(ind))
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
        if save_fn:
            plt.savefig('%s/%s.pdf' % (save_dir, save_fn))
        plt.show()

class one_pie_chart(object):
    def __init__(self, _title, per_data, _labels, save_fn=None):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        labels = []
        for i, l in enumerate(_labels):
            labels.append('%s (%.2f)' % (l, per_data[i]))
        ax.pie(per_data, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.legend(labels, fontsize='x-small')
        ax.set_title(_title)
        if save_fn:
            plt.savefig('%s/%s.pdf' % (save_dir, save_fn))
        plt.show()

class two_pie_chart(object):
    def __init__(self, _labels, title1, per_data1, title2, per_data2, save_fn=None):
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
        if save_fn:
            plt.savefig('%s/%s.pdf' % (save_dir, save_fn))
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

class horizontal_bar_chart(object):
    UNIT = 1.0
    HALF_UNIT = UNIT / 2
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    FIG_SIZE_UNIT = 6
    def __init__(self, main_name, sub_name, x_data):
        fig = plt.figure(figsize=(grid_charts.FIG_SIZE_UNIT, grid_charts.FIG_SIZE_UNIT))
        paths = []
        xs, ys = [], []
        for i in xrange(len(x_data)):
            x, y = x_data[i], i
            xs.append(x); ys.append(y)
            if x >= 0 :
                left_bottom = (0, y - grid_charts.HALF_UNIT) 
                left_top = (0, y + grid_charts.HALF_UNIT)
                right_top = (x, y + grid_charts.HALF_UNIT)
                right_bottom = (x, y - grid_charts.HALF_UNIT)
                ignored = left_bottom
                verts = [left_bottom, left_top  , right_top , right_bottom, ignored]
            else:
                left_bottom = (x, y - grid_charts.HALF_UNIT) 
                left_top = (x, y + grid_charts.HALF_UNIT)
                right_top = (0, y + grid_charts.HALF_UNIT)
                right_bottom = (0, y - grid_charts.HALF_UNIT)
                ignored = left_bottom
                verts = [left_bottom, left_top  , right_top , right_bottom, ignored]
            paths.append(Path(verts, grid_charts.codes))
        ax = fig.add_subplot(111)
        for i, path in enumerate(paths):
            patch = patches.PathPatch(path, facecolor=clists[0])
            ax.add_patch(patch)
        ax.set_xlim(min(xs) - grid_charts.HALF_UNIT, max(xs) + grid_charts.HALF_UNIT)
        ax.set_ylim(min(ys) - grid_charts.HALF_UNIT, max(ys) + grid_charts.HALF_UNIT)
        plt.yticks([int(len(ys) * 0.00), int(len(ys) * 0.25), int(len(ys) * 0.50), int(len(ys) * 0.75), int(len(ys) * 1.00)], ['0%', '25%', '50%', '75%', '100%'])
        # TODO
        # Modify saving part
        plt.savefig('%s-%s.pdf' % (main_name, sub_name))
#         plt.show()

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
        print colors_set
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
        if title: plt.text(0.5, 1.08, title, horizontalalignment='center', transform=ax.transAxes)
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
    
    
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z ** 2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    
    l = [[zip(x, y, z), 'test']]
    line_3D((6, 6), '', '', '', l)
    
#     , _figsize, _title, _xlabel, _ylabel, _data
    
if __name__ == '__main__':
    test()
