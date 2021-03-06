#!/usr/bin/python 

import sys  
import commands
import logging
import os 
from cgi import escape 

# basic setup
sys.stderr = sys.stdout
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

# little htpasswd test
me = commands.getoutput('/usr/bin/whoami')
cmd = '/usr/bin/htpasswd -b /etc/apache2/passwd/eamm.passwd test11 test11'   
(ret_code, ret_text) = commands.getstatusoutput(cmd)

# log return codes.
logging.info("ret_code: %s" % ret_code)
logging.info("ret_text: %s" %ret_text)

print "Content-type: text/html" 
print 
print "<html><head>"
print "<link rel=stylesheet type=text/css href=\"/eamm/css/eamm.css\">"
print "<title>EAMM :: Environment Variables</title></head><body><p>" 
print "Running:" 
print "<b>Python %s</b><br><br>" %(sys.version) 
print "<b> User: %s</b><br><br>" % me
print "Environmental variables:<br>" 
print "<ul>" 

for k in sorted(os.environ): 
	print "<li><b>%s:</b>\t\t%s<br>" %(escape(k), escape(os.environ[k])) 

print "</ul></p></body></html>"
