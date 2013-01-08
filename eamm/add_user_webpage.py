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

import eamm.base_webpage 
import eamm.user

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)
import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class AddUserWebPage(eamm.base_webpage.WebPage):

    """This class provides website/html components for Adding Users to the application.

    Public Attributes:
        none.
    Public Methods:
        display_add_user_form()
        process_add_user_form()
    """
    
    def __init__(self):
        """Constructor, sets all initial values to NULL.

        Args:
            none.
        Returns:
             AddUserWebPage object.
        Raises:
            none.
        """
        super(AddUserWebPage, self).__init__()
        
    def display_add_user_form(self):
        """This is the externally called method when HTTP method is GET

        Args:
            none.
        Returns:
            none (prints out the webpage)
        Raises:
            none, errors raised in the subclasses.
        """       

        self.set_title("Add User")
        
        add_user_form = """
        
        <p>
        
        <form name="main" method="POST" action="/eamm/add_user.py"> 
        
        <table width="400" border="border" align="center" bgcolor="#1E90FF">
          <tr>
            <td>Full Name:</td>
            <td><input type="text" colspan="30" id="Full Name" name="Full Name"/><td>
          </tr>
          <tr>
            <td>Email Address:</td>
            <td><input type="text" colspan="30" id="Email Addr" name="Email Addr"/></td>
          </tr>
          <tr>
            <td>username:</td>
            <td><input type="text" colspan="30" id="username" name="username"/></td>
          </tr>
          <tr>
            <td>password:</td> 
            <td><input type="password" colspan="30" id="password" name="password"/></td>
          </tr>
          <tr>
            <td width="100%"><input type="submit" value="Submit" /><td>
          </tr>
        </table>  
        
        """

        self.add_to_body(add_user_form)
        self.render()
        
    def process_add_user_form(self):
        """This is the externally called method when HTTP method is POST

        Args:
            none (though it pulls/uses the form contents.
        Returns:
            none (prints out the webpage)
        Raises:
            none, errors raised in the subclasses.
        """    
        
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
        
        logging.info("full_name: ", full_name, " email_addr: ", email_addr)
            
        # returns False is the account is not registered, returns the username or email_addr if either one is
        # already registered. If both registered, both returned.
        this_user = eamm.user.User()
        response = this_user.is_already_registered(email_addr, username)
        if response == True:
            user_message = "Error: is already registered, try again"
            user_message = self.error_table(user_message)
            self.add_to_body(user_message)
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