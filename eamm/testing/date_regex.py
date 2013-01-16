#!/usr/bin/python

import re

def main():
    my_date = "2013-01-01"

    # result = re.match(pattern, string)
    result = re.match(r"^20\d\d-([01]\d)-([0-3]\d$)", my_date)
    
    #crap = result.group(1)
    #print(crap)
    
    if result == None:
        print("match not found")
    else:
        print("match found")
        if (int(result.group(1)) > 12):
            print "but month is to big"
        if (int(result.group(2)) > 31):
            print "but date is too big (%s)" % result.group(2)
        else:
            print "date is OK (%s)" % int(result.group(2))
        
    #print("result: %s" % result)

if __name__ == '__main__':
    main()