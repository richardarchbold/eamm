#!/usr/bin/python

from datetime import datetime, timedelta

import re

def main():
    # ok, weekly recurring meetings, can't be to hard to figure out dates.
    # we have a start_datetime and end_datetime from form.
    # we also have start_date and end_date from the form.
    #
    # while (start_date <= end_date):
    #    meeting.add(foo, bar, etc)
    #    start_date += 7 days
    
    # set up initial variables.
    start_datetime = "2013-01-01 11:00"
    end_datetime   = "2013-01-28 11:45"
    start_date     = "2013-01-01"
    end_date       = "2013-01-31"
    start_time     = "11:00"
    duration       = 45
    
    dt_start   = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M")
    dt_end     = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M")
    
    while (dt_start <= dt_end):
        mt_start = dt_start
        mt_end   = dt_start + timedelta(minutes=duration)
        print "start: %s" % mt_start
        print "end:   %s" % mt_end
        print ""
        
        dt_start += timedelta(days=7)
       
if __name__ == '__main__':
    main()
    
    