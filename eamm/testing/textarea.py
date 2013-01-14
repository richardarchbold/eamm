#!/usr/bin/python

import cgi
# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

def main():
    form = cgi.FieldStorage()
    my_txt = form.getvalue('test')
    
    print "Content-type:text/html\r\n\r\n"
    print "<html>"
    print "<head>"
    print "</head>"
    print "<body>" 
    print "my_txt = %r" % my_txt
    print "</body>"
    print "</html>\r\n\r\n"

if __name__ == '__main__':
    main()