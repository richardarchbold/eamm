#!/usr/bin/python

from datetime import datetime, timedelta

def main():
    buffer_mins = 15
    now = datetime.now()
    new = now - timedelta(minutes=buffer_mins)
    new.strftime("%Y-%m-%d %H:%M:%S") 
    print(new.replace(microsecond=0))
    print(new.strftime("%Y-%m-%d %H:%M:%S"))
    
if __name__ == '__main__':
    main()