"""The module provides website/HTML functionality for user manager..

  Class:
      AddUserWebPage: The main class this module provides, extends base_webpage.WebPage
      
Source: https://github.com/richardarchbold/eamm
Created: 3 Jan 2013
"""

__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

import eamm.frontend.base_webpage 
import eamm.backend.user

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)
import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class AddUserWebPage(eamm.frontend.base_webpage.WebPage):
   
    def __init__(self):
        super(AddUserWebPage, self).__init__()
        
    def display_add_user_form(self):
        self.set_title("Add User")   
        add_user_form = """
        <form name="add_user" method="post" action="/eamm/add_user.py"> 
        <table>
          <tr>
            <td class="col1">Full Name:</td>
            <td class="col2_top"><input type="text" size="50" name="Full Name"/></td>
          </tr>
          <tr>
            <td class="col1">Email Address:</td>
            <td class="col2_top"><input type="text" size="50" name="Email Addr"/></td>
          </tr>
          <tr>
            <td class="col1">username:</td>
            <td class="col2_top"><input type="text" size="50" name="username"/></td>
          </tr>
          <tr>
            <td class="col1">password:</td> 
            <td class="col2_top"><input type="password" size="50" id="password" name="password"/></td>
          </tr>
          <tr>
            <td colspan="2" class="header"><input type="submit" value="Submit" /></td>
          </tr>
        </table>  
        </form>
        """
        self.add_to_body(add_user_form)
        self.render()
        
    def process_add_user_form(self):
        self.set_title("Add User :: Results")   
        form = cgi.FieldStorage()
        
        if form.getvalue('Full Name'):
            full_name = form.getvalue('Full Name')
        if form.getvalue('Email Addr'):
            email_addr = form.getvalue('Email Addr')
        if form.getvalue('Full Name'):
            username = form.getvalue('username')
        if form.getvalue('Email Addr'):
            password = form.getvalue('password')
      
        if not all((full_name, email_addr, username, password)):
            self.add_to_body(self.error_table("Error: all fields must be filled in, try again"))  
        
        logging.info("full_name: ", full_name, " email_addr: ", email_addr)
            
        # returns False is the account is not registered, returns the username or email_addr if either one is
        # already registered. If both registered, both returned.
        this_user = eamm.backend.user.User()
        response = this_user.is_already_registered(email_addr, username)
        
        if response == True:
            self.add_to_body(self.error_table("Error: is already registered, try again"))
            self.render()
        else:
            # returns True if successful, returns an error if unsuccessful.
            response2 = this_user.add_user(full_name, email_addr, username, password)
            if response2 != True:
                user_message = "Error: " + response2 
                self.render()
            else:
                user_message = "Success! %s, you account is now active" % full_name
                user_message = self.simple_table(user_message)
                self.add_to_body(user_message)
                self.render()    