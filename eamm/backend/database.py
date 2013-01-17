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

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class MyDatabase(object):

    """Class to connect to the local MySQL instance.
    
    MySQLdb is the module we are using as our MySQL connector
    see http://www.tutorialspoint.com/python/python_database_access.htm 
    for details on how this package works.
    
    Public Attributes:
        rows: the list of tuples that are returned from a fetchall() call
    Public Methods
       select(): used to execute an SQL select statement.
       insert(): used to execute an SQL insert statement. 
    """ 

    def __init__(self):
        """Constructor, main function is to initialize the DB connection.

        Args:
            none.
        Returns:
            none.
        Raises:
            MySQLdb.connect error.
        """
        db_host = "localhost"
        db_user = "eamm"
        db_pass = "eamm123pw"
        db_name = "EAMM"
        
        try:
            self.db = MySQLdb.connect (host = db_host, 
                                       user = db_user,
                                       passwd = db_pass,
                                       db = db_name)
        except:
            logging.info("MySQLdb.connect failed")
            raise

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
        except:
            logging.info("MySQLdb.select(%s) failed" % select_stmt)
            raise
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
                for i in len(sql_vars):
                    logging.info("sql_vars[%s] = %s" % (i, sql_vars[i]))
                try:
                    cursor.execute(select_stmt, tuple(sql_vars))  
                except:
                    logging.info("MySQLdb.select(%s) failed while using sql_vars" % select_stmt)
                    raise
        else:    
            logging.info("SELECT2: *was not* passed a list of variables for substitution")
            try:
                cursor.execute(select_stmt)  
            except:
                logging.info("MySQLdb.select(%s) failed" % select_stmt)
                raise
            
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
            none.
        Raises:
            MySQLdb.execute error.
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
        except:
            # Rollback in case there is any error
            self.db.rollback()
            raise

        # disconnect from server
        self.db.close()
        
        if auto_increment:
            return id
        

    def delete(self, delete_stmt):
        logging.info("DELETE:\n%s" % delete_stmt)
        try:
            # Execute the SQL command
            cursor = self.db.cursor()
            cursor.execute(delete_stmt)
            # Commit your changes in the database
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()
            raise

        # disconnect from server
        self.db.close()