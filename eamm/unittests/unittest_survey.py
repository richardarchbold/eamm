import eamm.backend.survey
import unittest

class TestBackendInvite(unittest.TestCase):

    def test_get_questions(self):
        id_template = 1
        my_questions = eamm.backend.survey.get_questions(id_template)
        self.assertTrue(len(my_questions) >= 9)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()