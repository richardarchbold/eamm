#!/usr/bin/python

def is_weekday(date):
    pass

start_date  = 16 (wed)
end_date    = 30

# recur daily
date = start_date
while date <= end_date:
    if is_weekday(date):
        print(date)
    date += 1

# recur weekly
date = start_date
while date <= end_date:
    print(date)
    date += 7
    
# recur monthly (recur on the Xth <weekday> of the month)
# xth = roundup(start_date/7)

