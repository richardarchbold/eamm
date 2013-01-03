'''
Created on 3 Jan 2013

@author: richard
'''
#!/usr/bin/env python

class WebPage(object):
    
    def __init__(self):
        self.title = "EAMM ::"
        self.body = ""
        self.bgcolor = "#E6E6FA"
        
    def set_title(self, title):
        self.title = self.title + ' ' + title
        
    def add_to_body(self, body):
        self.body = self.body + ' ' + body
        
    def render(self):
        print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
        print "<title> %s </title>" % self.title
        print "</head>"
        print "<body bgcolor=\"%s\">" % self.bgcolor
        print self.body
        print "</body>"
        print "</html>\r\n\r\n"
        