#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")
import eamm.frontend.survey_webpage
import unittest

class TestEammFrontendSurveyWebpage(unittest.TestCase):

    def test_parse_query_string1(self):
        my_page1 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page1.query_string = "var1=12345&var2=rich%40amazon.com"
        
        return_value = my_page1.parse_query_string() 
        self.assertTrue(return_value)

    def test_parse_query_string2(self):
        my_page2 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page2.query_string = "var1=12345&var2=rich@amazon.com"
        return_value = my_page2.parse_query_string() 
        self.assertTrue(return_value)

    def test_parse_query_string3(self):
        my_page3 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page3.query_string = "var1=12345&var2=rich@amazon.com&var3=sfsdfs"
        return_value = my_page3.parse_query_string() 
        self.assertTrue(return_value)
    
    def test_parse_query_string4(self):
        my_page4 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page4.query_string = "var1=12d345&var2=rich@amazon.com"
        return_value = my_page4.parse_query_string() 
        self.assertFalse(return_value)

    def test_parse_query_string5(self):
        my_page5 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page5.query_string = "var1=12345&var2=richamazon.com"
        return_value = my_page5.parse_query_string() 
        self.assertFalse(return_value)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()