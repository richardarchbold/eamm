#!/usr/bin/python

import MySQLdb

def main():
    db_host = "localhost"
    db_user = "eamm"
    db_pass = "eamm123pw"
    db_name = "test"

    
    sql = """
    insert into tbl1 (col2, col3) values ('a', 'aaaaaaa')  
    """
    
    db = MySQLdb.connect (host = db_host, 
                          user = db_user,
                          passwd = db_pass,
                          db = db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    
    print("row type is: %s" % type(row))
    print("row[0]: %s" % row[0])
    
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()