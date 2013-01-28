import eamm.backend.database
import logging

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

def get_questions(id_template):

    # 1. get all initial generic questions.
    # 2. get template specific question.
    # 3. get all ending generic questions.
    # 4. return a dict, tupe of tuples with results ordered by idSurveyQuestion
    sql = """
    SELECT idSurveyQuestion, survey_question_text, idMeetingTemplate, ask_to_all 
    FROM EAMM.SurveyQuestion
    WHERE ask_to_all=1 or idMeetingTemplate=%s
    ORDER BY idSurveyQuestion
    """ 
    sql_vars=[id_template]
    
    db_conn = eamm.backend.database.MyDatabase()
    my_query_results = db_conn.select2(sql, sql_vars)
    if not my_query_results:
        logging.info(db_conn.error)
        return False
    elif len(my_query_results) == 0:
        logging.info("bad sql, not exist")
        return False
    else:
        # looks like were good.
        return my_query_results

class Survey(object):
    def __init__(self):
        pass
    
    
        