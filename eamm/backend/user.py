"""The user module provides business logic functionality to the main EAMM application.

This modules provides basic user management functionality. It uses the database class as
an abstraction layer to communicate with the mysql instance.

  Class:
      User: The main class this module provides.
      
Source: https://github.com/richardarchbold/eamm
Created: 3 Jan 2013
"""

__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

import eamm.backend.database
import logging
import commands

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class User(object):

    """This class provides business logic for adding/updating/viewing eamm application users.

    Public Attributes:
        none.
    Public Methods:
        add_user:(full_name, email_addr, username, password)
        is_already_registered(email_addr, username)
    """

    def __init__(self):
        """Constructor, sets all initial valies to NULL.

        Args:
            none.
        Returns:
            User object.
        Raises:
            none.
        """

        self.full_name = ""
        self.email_addr = ""
        self.username = ""
        self.password = ""
    
    def add_user(self, full_name, email_addr, username, password):
        """A one line summary of the function/method, eg: Fetch rows from a table.
       
        Args:
            Arg1: description
            Arg2: description
           row to fetch.
        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """

        cmd = '/usr/bin/htpasswd -b /etc/apache2/passwd/eamm.passwd %s %s' % (email_addr, password)
        (ret_code, ret_text) = commands.getstatusoutput(cmd)
        
        if (ret_code != 0):
            logging.info("Couldn't add user to htpasswd file - %s" % ret_text)
            return False

        sql = "insert into User (full_name, email_addr, username, password) values ('%s', '%s', '%s', '%s')" % (full_name, email_addr, username, password)
    
        # no need to try/catch/rasie these, as the subclass takes care of that.
        my_db_connection = eamm.backend.database.MyDatabase()
        my_db_connection.insert(sql)
        
        # now add to htaccess file.
        # /usr/bin/htpasswd -b email_addr password
        # /usr/bin/htpasswd -b username password
        cmd = '/usr/bin/htpasswd -b %s %s' % (email_addr, password)
        ret = commands.getstatusoutput(cmd)
        
        return True
    
    def is_already_registered(self, email_addr, username):
        """Checks to see if an email_addr or username is already registered in the Users tables.

        Args:
            email_addr: email address of the user you're checking.
            username: username of the user you're checking.
        Returns:
            my_query_results: a dict of tuples.
        Raises:
            none, errors raised in the subclasses.
        """       

        sql = "select count(*) from User where (email_addr = '%s' or username = '%s')" % (email_addr, username)
        my_db_connection = eamm.backend.database.MyDatabase()
        my_query_results = my_db_connection.select(sql)        # my_query_results is a dict of tuples.
        logging.info(my_query_results[0][0])
            
        if my_query_results[0][0] == 0:
            return False
        else:
            return True 
        