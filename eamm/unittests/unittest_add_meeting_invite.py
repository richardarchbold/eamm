import sys
sys.path.append("/home/richard/workspace/eamm/")

import unittest
import urllib, urllib2
import re
import eamm.backend.database

class Test(unittest.TestCase):

    def setUp(self):
        # get the idInvite of the test record.
        db_conn = eamm.backend.database.MyDatabase()
        sql = """
        select idInvite from EAMM.Invite
        where purpose like '%test%'
          and requester_email_addr = 'keepitreal@eircom.net'
          and start_date >= '2018-01-01'
        """
        rows = db_conn.select2(sql)
        
        # fixme, now we need to delete all test data in 2018
        if (len(rows) > 0):
            # if we get this far, lets do the remainder of the delete calls
            # as a transaction.
            db_conn = eamm.backend.database.MyDatabase()
            db_conn.autocommit = False
            
            for row in rows:
                id_invite = row[0]
                sql_vars = [id_invite]
                
                # delete test records from Invite table.            
      
                sql = """
                delete from EAMM.Invite
                where idInvite=%s 
                limit 1
                """
                db_conn.delete(sql, sql_vars)
    
                # delete test records from Invitee table.
                sql = """
                delete from EAMM.Invitee
                where idInvite=%s
                """
                db_conn.delete(sql, sql_vars)
    
                # delete test records from Meeting table.
                sql = """
                delete from EAMM.Meeting
                where idInvite=%s
                """
                db_conn.delete(sql, sql_vars)

            # commit
            db_conn.db.commit()
    
    # no recurrence.
    def testAddMeetingViaForm1(self):
        # this is the page we are testing.
        url = 'http://127.0.0.1/eamm/private/add_meeting_invite.py'
        
        # setup everything we need to get past BasicAuth
        username = 'test'
        password = 'test-pass'
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        urllib2.install_opener(urllib2.build_opener(
                                        urllib2.HTTPBasicAuthHandler(passman)))

        # setup the params of the meeting we are trying to save.
        raw_params = {
                      'step': 'step4',
                      'purpose': "test purpose",
                      'justification': "test justification",
                      'template': "2",
                      'agenda': "test agenda",
                      'title': "test title",
                      'start_date': "2018-01-01",
                      'start_time': "20:00",
                      'duration': "40",
                      'recurring': "none",
                      'venue': "test venue",
                      'requester': "keepitreal@eircom.net",
                      'invitees': "<p>keepitreal@eircom.com</p>"
                     }
        params = urllib.urlencode(raw_params)

        # post to the page.
        request = urllib2.Request(url, params)
        page = urllib2.urlopen(request)
        
        # parse the response to make sure the meeting appears to have been
        # added.
        html = page.read()
        #print html
        match = re.search('Your meeting invite has been saved on the system', 
                          html)
        self.assertTrue(match)

    # daily recurrence.
    def testAddMeetingViaForm2(self):
        # this is the page we are testing.
        url = 'http://127.0.0.1/eamm/private/add_meeting_invite.py'
        
        # setup everything we need to get past BasicAuth
        username = 'test'
        password = 'test-pass'
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        urllib2.install_opener(urllib2.build_opener(
                                        urllib2.HTTPBasicAuthHandler(passman)))

        # setup the params of the meeting we are trying to save.
        raw_params = {
                      'step': 'step4',
                      'purpose': "test purpose",
                      'justification': "test justification",
                      'template': "2",
                      'agenda': "test agenda",
                      'title': "test title daily recurring",
                      'start_date': "2018-01-01",
                      'end_date': "2018-01-30",
                      'start_time': "17:00",
                      'duration': "40",
                      'recurring': "daily",
                      'venue': "test venue",
                      'requester': "keepitreal@eircom.net",
                      'invitees': "<p>keepitreal@eircom.com</p>"
                     }
        params = urllib.urlencode(raw_params)

        # post to the page.
        request = urllib2.Request(url, params)
        page = urllib2.urlopen(request)
        
        # parse the response to make sure the meeting appears to have been
        # added.
        html = page.read()
        #print html
        match = re.search('Your meeting invite has been saved on the system', 
                          html)
        self.assertTrue(match)

    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()