'''
Created on 3 Jan 2013

@author: richard
'''

from eamm.base_webpage import *
from eamm.user import *

# Import modules for CGI handling 
import cgi
import cgitb; cgitb.enable(display=1)

class AddUserWebPage(WebPage):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        We use the super built-in because we need to.
        '''
        super(AddUserWebPage, self).__init__()
        
    def display_add_user_form(self):
        '''
        this is the externally called method when HTTP method is GET
        '''
        self.set_title("Add User")
        
        add_user_form = """
        <p>
        <form name="main" method="POST" action="/eamm/add_user.py"> 
        Full Name: <input type="text" id="Full Name" name="Full Name"/><br>
        Email Address: <input type="text" id="Email Addr" name="Email Addr"/><br>
        username: <input type="text" id="username" name="username"/><br>
        password: <input type="password" id="password" name="password"/><br>
        <input type="submit" value="Submit" />
        <p>
        """

        self.add_to_body(add_user_form)
        self.render()
        
    def process_add_user_form(self):
        '''
        this is the externally called method when the HTTP method is POST
        '''
        self.set_title("Add User :: Results")
        
        my_debug = True
                       
        form = cgi.FieldStorage()
        
        if form.getvalue('Full Name'):
            full_name = form.getvalue('Full Name')
        if form.getvalue('Email Addr'):
            email_addr = form.getvalue('Email Addr')
        if form.getvalue('Full Name'):
            username = form.getvalue('username')
        if form.getvalue('Email Addr'):
            password = form.getvalue('password')
        
        if my_debug:
            form_foo = "<p><p> full_name: " + full_name + "\n email_addr" + email_addr + "<p><p>"
            self.add_to_body(form_foo)
            
        # returns False is the account is not registered, returns the username or email_addr if either one is
        # already registered. If both registered, both returned.
        this_user = User()
        response = this_user.is_already_registered(email_addr, username)
        if response != False:
            user_message = "Error: " + response + " is already registered, try again"
            self.add_to_body(user_message)
            self.render()
        else:
            # returns True if successful, returns an error if unsuccessful.
            
            response2 = this_user.add_user(full_name, email_addr, username, password)
            if response2 != True:
                user_message = "Error: " + response2 
                self.render()
            else:
                user_message = "Success!"
                self.render()
                
    
        