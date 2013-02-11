#!/usr/bin/python

import datetime

def main():
    d1 = datetime.datetime(2013,2,11)
    d2 = datetime.datetime(2014,01,01)

    my_dates = recurr_every_X_months(d1, d2, 3)
    
    for d in my_dates:
        print d
    
def recurr_every_X_months(d1, d2, m):
    
    dlist = list()     
    d_temp = d1
    n = 4
    count = 0
    
    while d_temp <= d2:
        if count % m == 0:
            dlist.append(d_temp)
        count += 1
        d_temp =  _next_month(d_temp, n)

    return dlist

def _next_month(d, n):
    d_next = d + datetime.timedelta(weeks=n)
    if _weekday_index(d_next) < _weekday_index(d):
        d_next += datetime.timedelta(weeks=1)
    return d_next

def _weekday_index(d):
    return (d.day + 6) // 7
    
if __name__ == '__main__':
    main()