#!/usr/bin/python

import unittest
import eamm.backend.meeting_invite

class TestBackendMeetingInvite(unittest.TestCase):

    def testInit1(self):
        test_id_invite = 1
        my_invite = eamm.backend.meeting_invite.MeetingInvite(test_id_invite)
        self.assertTrue((my_invite.is_valid) and 
                        (my_invite.title == "my test title xyz") and
                        (my_invite.invitees_list[1] == "b@b.com"))
        
    def testInit2(self):
        test_id_invite = -1
        my_invite = eamm.backend.meeting_invite.MeetingInvite(test_id_invite)
        self.assertTrue(my_invite.is_valid == False)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()