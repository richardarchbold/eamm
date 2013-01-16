

#!/usr/bin/python

import dateutil.rrule as dr
import dateutil.parser as dp
import dateutil.relativedelta as drel

def main():
    #start=dp.parse("16/01/2013")   # Third Wednesday in Jan
    start=dp.parse("2013-02-16")
    
    rr = dr.rrule(dr.MONTHLY,byweekday=drel.FR(3),dtstart=start, count=2)
    print map(str,rr)
    

if __name__ == '__main__':
    main()
    
    