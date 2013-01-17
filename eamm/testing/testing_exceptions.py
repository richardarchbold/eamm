#!/usr/bin/python

from os.path import basename

def main():
    try:
        1/0
    except Exception, e:
        error = str(e)
   
    print("Error is , %s" % ( error))
    f = basename(__file__)
    print(f)

if __name__ == '__main__':
    main()