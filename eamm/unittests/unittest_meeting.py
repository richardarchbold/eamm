#! /usr/bin/python

import unittest
import eamm.backend.meeting

class TestBackendMeeting(unittest.TestCase):

    def testInit1(self):
        test_id_meeting = 24
        my_meeting = eamm.backend.meeting.Meeting(test_id_meeting)
        self.assertTrue(my_meeting.is_valid and (my_meeting.id_invite == 1))
        
    def testInit2(self):
        test_id_meeting = -1
        my_meeting = eamm.backend.meeting.Meeting(test_id_meeting)
        self.assertTrue(my_meeting.is_valid == False)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()