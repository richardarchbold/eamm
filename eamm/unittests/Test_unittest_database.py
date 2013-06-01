import eamm.backend.database
import unittest

class TestEammBackendDatabase(unittest.TestCase):
    
    def setUp(self):
        db_conn = eamm.backend.database.MyDatabase()
        sql = "delete from EAMM.unittest where test_col1 like '%testing122%'"
        db_conn.delete(sql)
    
    def testInstantiation(self):
        test_db_connection = eamm.backend.database.MyDatabase()
        self.assertTrue(test_db_connection.is_valid, "Could not log into DB")
        
    def testInsertAutoIncrement(self):
        sql = """insert into EAMM.unittest (test_col1) values (%s)"""
        sql_vars = ["testing122"]
        
        test_db_connection_1 = eamm.backend.database.MyDatabase()
        my_insert_id = test_db_connection_1.insert2(sql, sql_vars, True)
        
        # if the insert with autoincrement worked, my_insert_id will be an int, greater than zero
        self.assertTrue(my_insert_id>0)
    
    def testSelect(self):
        sql = """ select count(*) from EAMM.unittest where test_col1=%s """
        sql_vars = ["testing123"]
        
        test_db_connection_2 = eamm.backend.database.MyDatabase()
        my_query_results = test_db_connection_2.select2(sql, sql_vars)
        self.assertTrue(my_query_results[0][0] == 1)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()