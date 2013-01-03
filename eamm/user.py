'''
Created on 3 Jan 2013

@author: richard
'''

#!/usr/bin/env python

class User(object):
    def __init__(self):
        self.full_name = ""
        self.email_addr = ""
        self.username = ""
        self.password = ""
    
    def add_user(self, full_name, email_addr, username, password):
        return True
    
    def is_already_registered(self, email_add, username):
        return False