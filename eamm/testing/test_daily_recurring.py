#!/usr/bin/python

#from dateutil.relativedelta import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

def main():
    # recurring daily
    print "***** DAILY RECURRING *****"
    my_dates = list(rrule(DAILY, 
                          byweekday=(MO,TU,WE,TH,FR),
                          dtstart=datetime(2013,2,11),
                          until=datetime(2013,2,21),
                          count=2 # count overrides 'until' flag
                          )
                    )
    
    for my_date in my_dates:
        print my_date
        
    # recurring monthly
    print "***** MONTHLY RECURRING *****"
    
    (YYYY, MM, DD) = (2013,2,11)
    sd = datetime(YYYY,MM,DD)
    
    # day of the week in rrule format.
    # use strftime (string from time) to get the weekday's day, convert it to
    # upper case and then return the first 2 chars.
    dy = sd.strftime('%a').upper()[:2]
    
    # divide the day of the month by 7:
    # if < 1, then first X of the month,
    # if >1 <2, then second X of the month, etc.
    x = int(DD/7)+1
    
    rrule_flag = "%s(%s)" % (dy, x)
    print "weekday = %s" % rrule_flag
    
    my_dates2 = list(rrule(MONTHLY, 
                           count=10, 
                           byweekday=MO(x),
                           dtstart=sd,
                           )
                     )
    
    for my_date2 in my_dates2:
        print my_date2
    
if __name__ == '__main__':
    main()