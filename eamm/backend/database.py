"""This module is the database abstraction layer for the EAMM application.

The database module is used to abstract away the type of database engine
is used by the application to store date. This makes it easier to switch 
db's in the future, only requiring one module to be updated.

  Class MyDatabase: The only Class in this module, connects to the local MySQL instance.

Source: https://github.com/richardarchbold/eamm
Created: 4 Jan 2013
"""

__authors__ = [
  '"Richard Archbold" <richardarchbold@gmail.com>',
]

import MySQLdb
import logging
from os.path import basename

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

# setup short filename for error reporting purposes
f = basename(__file__)

class MyDatabase(object):

    """Class to connect to the local MySQL instance.
    
    MySQLdb is the module we are using as our MySQL connector
    see http://www.tutorialspoint.com/python/python_database_access.htm 
    for details on how this package works. 
    """ 

    def __init__(self):
        """Constructor, main function is to initialize the DB connection.
        """
        db_host = "localhost"
        db_user = "eamm"
        db_pass = "eamm123pw"
        db_name = "EAMM"
        
        self.is_valid = True
        self.error = None
        
        try:
            self.db = MySQLdb.connect (host = db_host, 
                                       user = db_user,
                                       passwd = db_pass,
                                       db = db_name)
        except Exception as e:
            self.error = "Class: MyDatabase, Method: init, Message: %s" % str(e)
            logging.info(self.error)
            self.is_valid = False
        
        

    def select(self, select_stmt):
        """Execute a select statement against the DB.

        Args:
            select_stmt: a string containing the SQL command to be executed.
        Returns:
            rows: a dict containing the rows returned by the select 
        Raises:
            none.
        """
        logging.info("SELECT:\n%s " % select_stmt)
        try:
            cursor = self.db.cursor()
            cursor.execute(select_stmt)
            rows = cursor.fetchall()    
        except Exception as e:
            self.error = "Class: MyDatabase, Method: select, Message: %s" % str(e)
            logging.info(self.error)
            self.is_valid = False
            return False
        
        logging.info("SELECT: returned %s rows" % len(rows))
        cursor.close()
        self.db.close()
        return rows
    
    def select2(self, select_stmt, sql_vars=None):
        logging.info("SELECT2:\nsql:%s" % select_stmt)
        
        cursor = self.db.cursor()
        
        if sql_vars:
            if type(sql_vars) is list:
                logging.info("SELECT2: *was* passed a list of variables for substitution")
                count=0;
                while count < len(sql_vars):
                    logging.info("sql_vars[%s] = %s" % (count, sql_vars[count]))
                    count+=1
                try:
                    cursor.execute(select_stmt, tuple(sql_vars))  
                except Exception as e:
                    self.db.close()
                    self.error = "Class: MyDatabase, Method: select2, Message: %s" % str(e)
                    logging.info(self.error)
                    self.is_valid = False
                    return False
        else:    
            logging.info("SELECT2: *was not* passed a list of variables for substitution")
            try:
                cursor.execute(select_stmt)  
            except Exception as e:
                self.db.close()
                self.error = "Class: MyDatabase, Method: select2, Message: %s" % str(e)
                logging.info(self.error)
                self.is_valid = False
                return False
            
        rows = cursor.fetchall()
        logging.info("SELECT2: returned %s rows" % len(rows)) 
        cursor.close()
        self.db.close()
        return rows
    
    def insert(self, insert_stmt, auto_increment=None):
        """Execute an insert statement against the DB.

        Args:
            insert_stmt: a string containing the SQL command to be executed.
        Returns:
            
        """
        logging.info("INSERT:\n%s" % insert_stmt)
        try:
            # Execute the SQL command
            cursor = self.db.cursor()
            cursor.execute(insert_stmt)
            # Commit your changes in the database
            self.db.commit()
            if auto_increment:
                cursor.execute("SELECT LAST_INSERT_ID()")
                row = cursor.fetchone()
                my_id = row[0]
                logging.info("INSERT last auto_increment value: %s" % my_id)
        except Exception as e:
            # Rollback in case there is any error
            self.db.rollback()
            self.db.close()
            self.error = "Class: MyDatabase, Method: insert, Message: %s" % str(e)
            logging.info(self.error)
            self.is_valid = False
            return False

        # disconnect from server
        self.db.close()
        
        if auto_increment:
            return id
    
    def insert2(self, insert_stmt, sql_vars, auto_increment=None):
        logging.info("INSERT2:\n%s" % insert_stmt)
        
        if type(sql_vars) is list:
            logging.info("INSERT2: *was* passed a list of variables for substitution")
            count=0;
            while count < len(sql_vars):
                logging.info("sql_vars[%s] = %s" % (count, sql_vars[count]))
                count+=1
            try:
                cursor = self.db.cursor()
                cursor.execute(insert_stmt, tuple(sql_vars))  
                self.db.commit()
                if auto_increment:
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    row = cursor.fetchone()
                    my_id = row[0]
                    logging.info("INSERT last auto_increment value: %s" % my_id)
            except Exception as e:
                self.db.close()
                self.error = "Class: MyDatabase, Method: insert2, Message: %s" % str(e)
                logging.info(self.error)
                self.is_valid = False
                return False
        else:
            self.error = "Class: MyDatabase, Method: insert2, Message: INSERT2 was \
            passed a sql_vars arg that was not a list (%s)" % type(sql_vars)
            logging.info(self.error)
            self.is_valid = False
            return False
                
        # disconnect from server
        self.db.close()
        
        if auto_increment:
            return id
        else:
            return True
        
    def delete(self, delete_stmt):
        logging.info("DELETE:\n%s" % delete_stmt)
        try:
            # Execute the SQL command
            cursor = self.db.cursor()
            cursor.execute(delete_stmt)
            # Commit your changes in the database
            self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.db.rollback()
            self.error = "Class: MyDatabase, Method: delete, Message: %s" % str(e)
            logging.info(self.error)
            self.is_valid = False
            return False

        # disconnect from server
        self.db.close()
        return True