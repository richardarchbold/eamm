"""A one line summary of the module or script, terminated by a period.

Leave one blank line. The rest of this __doc__ string should contain an
overall description of the module or script.  Optionally, it may also
contain a brief description of exported classes and functions.

    ClassFoo: One line summary.
    functionBar(): One line summary.

Source:http://github/richardarchbold/eamm.git
Created: 7 Jan 2013
"""
__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

import eamm.database
import logging

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingTemplate(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Public  Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
     Public Methods:
         name:  1 line summary
     """
    
    def __init__(self):
        """A one line summary of the function/method, eg: Fetch rows from a table.

        Public Args:
            Arg1: description
            Arg2: description row to fetch.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """
    
    def get_all(self):
        
        sql = '''
        SELECT idMeetingTemplate, title, description, purpose, agenda FROM EAMM.Template 
            ORDER BY idMeetingTemplate;
        '''   
        
        my_db_connection = eamm.database.MyDatabase()
        my_query_results = my_db_connection.select(sql)        # my_query_results is a dict (tuple of tuples).
    
        if my_query_results[0][0] == 0:
            # this means the select got back nothing.
            return False
        else:
            return my_query_results