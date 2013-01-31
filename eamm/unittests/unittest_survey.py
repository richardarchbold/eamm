import eamm.backend.survey
import eamm.backend.database
import unittest

class TestBackendSurvey(unittest.TestCase):

    def setUp(self):
        db_conn = eamm.backend.database.MyDatabase()
        sql = """delete from EAMM.Survey where idMeeting=1 and 
                 invitee_email_addr='rich@rich.com' and
                 responder_email_addr='crap@crap.com'
        """
        db_conn.delete(sql)

    def test_get_questions1(self):
        id_template = 1
        my_questions = eamm.backend.survey.get_questions(id_template)
        self.assertTrue(len(my_questions) >= 9)
    
    # even with an obviously dodgy id_template2, we still get back the default
    # questions
    def test_get_questions2(self):
        id_template2 = 56789
        my_questions2 = eamm.backend.survey.get_questions(id_template2)
        self.assertTrue(my_questions2)

    # we haven't figured out how to test with POST yet, so this will have to do.
    def test_add1(self):
        # create a base object
        my_survey = eamm.backend.survey.SurveyResponse()
        error_msg = ""
        
        # rather than loading the test data from a form, we specify it directly.
        my_survey.id_invite = 2
        my_survey.id_meeting = 1
        my_survey.invitee_email_addr = "rich@rich.com"
        my_survey.responder_email_addr = "crap@crap.com"
        my_survey.q_and_a = dict()
        my_survey.q_and_a[1]  = 50
        my_survey.q_and_a[2]  = 25
        my_survey.q_and_a[3]  = 50
        my_survey.q_and_a[4]  = 75
        my_survey.q_and_a[7]  = 75
        my_survey.q_and_a[13] = 50
        
        # go ahead and add it, return value should be true.
        try:
            ret = my_survey.add()
        except Exception as e:
            error_msg = str(e)
            ret = False
            
        self.assertTrue(ret, error_msg)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()