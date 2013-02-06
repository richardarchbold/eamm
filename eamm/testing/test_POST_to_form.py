#!/usr/bin/python

import urllib, urllib2

def main():
    page = 'http://127.0.0.1/eamm/eamm/testing/test_form.py'
    raw_params = {'var1': 'rich_test'}
    params = urllib.urlencode(raw_params)
    request = urllib2.Request(page, params)
    page = urllib2.urlopen(request)
    info = page.info()
    print "=======\n%s" % info
    print "======="
    print page.read()
    
if __name__ == '__main__':
    main()