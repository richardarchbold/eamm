import eamm.backend.survey
import unittest

class TestBackendInvite(unittest.TestCase):

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

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()