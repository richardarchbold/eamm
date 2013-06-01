#!/usr/bin/python

from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def main():
    
    # setup the NumPy array
    datafile = "/home/richard/workspace/eamm/eamm/testing/foo2.csv"
    #print ('loading %s' % datafile)
    r = mlab.csv2rec(datafile)
    r.sort()
    print("%s" % r.date[0])
    
    # create a figure, basically a container for a number of axes.
    # an axes is one or more axis (like and x and a y axis)
    fig = plt.figure()
    plt.ylim(0,100)
    
    # 1. add the first axes (chart) to the figure
    ax = fig.add_subplot(111)
    ax.set_ylim(top=100, bottom=0)
    
    # 2. specify that the x-axis is a date and format it as such
    ax.xaxis_date()
    fig.autofmt_xdate(bottom=0.3, rotation=330, ha='right')
    
    # 2. plot the line
    line1 = ax.plot(r.date, r.meeting_instance_score)
    
    plt.axhline(y=65)

    # 3. do all necessary chart formatting.
    # 3.1 set x and y lables
    
    ax.set_xlabel('Dates', fontsize=14)
    ax.set_ylabel('Meeting Instance Score', fontsize=14, color='red')
    
    # 3.2 format the plotted line.
    plt.setp(line1, color='r', linewidth=2.0, marker='+',
             markeredgewidth=3.0, markersize=3.0,
             label='Meeting Instance Score', ls=':')

    # create a second chart, that shares the same x-axis as the first chart
    ax2 = ax.twinx()
    ax2.set_ylim(top=100, bottom=0)
    
    # do all the same stuff as we did to the first chart.
    line2 = ax2.plot(r.date, r.all_meetings_score, 'g^')
    ax2.set_ylabel('All Meetings Avg Score', fontsize=14, color='green')
    plt.setp(line2, color='g', linewidth=2.0, marker='+',
             markeredgewidth=3.0, markersize=3.0,
             label='Meeting Instance Score', ls=':')
    
    # 
    
    
    plt.show()
    #plt.savefig('foo3.png')
    
if __name__ == '__main__':
    main()