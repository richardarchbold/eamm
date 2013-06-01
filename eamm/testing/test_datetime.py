#!/usr/bin/python

from datetime import datetime, timedelta

import re

def main():
    # DB: test
    # tbl = tbl2
    # cols = (id, start, end, duration)
    #
    # what i want to be able to do is:
    # 1. take a start_date, a start_time and combine them for a start_datetime
    # 2. add a duration onto the start_datetime to get the end_datetime
    # 3. successfully insert this into the DB.
    
    start_date = "2013-01-31"
    start_time = "11:00"
    duration   = 8
    start_datetime = start_date + " " + start_time
    end_datetime = ""
    
    #               YYYY
    m = re.search('^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$', start_datetime)
    YYYY = int(m.group(1))
    MM   = int(m.group(2))
    DD   = int(m.group(3))
    hh   = int(m.group(4))
    mm   = int(m.group(5)) 
    
    if m:
        print("regex works, %s" % YYYY)
    else:
        print("regex does not work")
    
    # now = datetime.datetime(2003, 8, 4, 12, 30, 45) 
    t1 = datetime(YYYY, MM, DD, hh, mm)
    print("start_datetime: %s" % t1)
    
    td = timedelta(minutes=duration)
    t2 = t1 + td
    print("end_datetime: %s" % t2) 
    
    sql = """
    INSERT INTO test.tbl2 (start, end, duration) 
    VALUES (%s, %s, %s)
    """ % (start_datetime, end_datetime, duration)
    
    #print(sql)
    
if __name__ == '__main__':
    main()