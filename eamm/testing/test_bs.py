#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

f = urlopen('http://127.0.0.1/eamm/survey.py?var1=24&var2=test@test.com')
data = f.read()
f.close
soup = BeautifulSoup(data)

#print soup.title
text = soup.title.string
print data


match = re.search('Meeting Effectiveness Survey', data)

if match:
    print "OK"
