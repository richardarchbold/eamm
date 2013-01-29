#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

import eamm.frontend.survey_webpage
import urllib2
import unittest
import re


class TestEammFrontendSurveyWebpage(unittest.TestCase):

    # test with a good query string, the @ symbol is encoded correctly.
    def test_parse_query_string1(self):
        my_page1 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page1.query_string = "var1=12345&var2=rich%40amazon.com"
        return_value = my_page1.parse_query_string() 
        self.assertTrue(return_value)

    # test with a good query string, the @ symbol is not encoded.
    def test_parse_query_string2(self):
        my_page2 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page2.query_string = "var1=12345&var2=rich@amazon.com"
        return_value = my_page2.parse_query_string() 
        self.assertTrue(return_value)

    # test with a bad query string, an extra var is added at the end.
    def test_parse_query_string3(self):
        my_page3 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page3.query_string = "var1=12345&var2=rich@amazon.com&var3=sfsdfs"
        return_value = my_page3.parse_query_string() 
        self.assertTrue(return_value)
    
    # test with a bad query string, plausible badness.
    def test_parse_query_string4(self):
        my_page4 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page4.query_string = "var1=12d345&var2=rich@amazon.com"
        return_value = my_page4.parse_query_string() 
        self.assertFalse(return_value)
    
    # test with a bad query string, more plausible badness.
    def test_parse_query_string5(self):
        my_page5 = eamm.frontend.survey_webpage.SurveyWebpage()
        my_page5.query_string = "var1=12345&var2=richamazon.com"
        return_value = my_page5.parse_query_string() 
        self.assertFalse(return_value)
    
    # test that the URL is returning a 200 error code, which it pretty much 
    # always should be if we are using "import cgitb; cgitb.enable(display=1)"
    def test_show_survey1(self):
        ok = True
        error = None
        url = 'http://127.0.0.1/eamm/complete_survey.py?var1=24&var2=test@test.com'
        request = urllib2.Request(url)
        try:
            urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            error = e.code
            ok = False 
        self.assertTrue(ok, "HTTP error code %s" % error)
    
    def test_show_survey2(self):
        url = 'http://127.0.0.1/eamm/complete_survey.py?var1=24&var2=test@test.com'
        f = urllib2.urlopen(url)
        data = f.read()
        f.close
        match = re.search('my test title xyz', data)
        self.assertTrue(match)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()