#!/usr/bin/python

import MySQLdb

def main():
    db_host = "localhost"
    db_user = "eamm"
    db_pass = "eamm123pw"
    db_name = "test"

    
    select_stmt = """
    SELECT * from test.tbl1 where idtbl1=%s AND col2=%s AND col3=%s 
    """
    var1 = "a'a"
    var2 = "b"
    var3 = """c'"c"""
    
    sql_vars = [var1, var2, var3]
    
    print(sql_vars)
    print(select_stmt % tuple(sql_vars))
    
    try:
        db = MySQLdb.connect (host = db_host, 
                              user = db_user,
                              passwd = db_pass,
                              db = db_name)
        cursor = db.cursor()
        cursor.execute(select_stmt, tuple(sql_vars))
        rows = cursor.fetchone()
        print ("row: %s, %s, %s" % tuple(rows))    
    except:
        raise
    
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()