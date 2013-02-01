import eamm.backend.database

def get_tot_avg_score(user):
    db_conn = eamm.backend.database.MyDatabase()
    sql = """
    SELECT avg(s.survey_response_rating)
    FROM EAMM.Meeting as m INNER JOIN EAMM.Invite as i INNER JOIN EAMM.Survey as s
    WHERE m.meeting_chair=%s 
    and   s.survey_response_rating != 0
    and   m.idInvite = i.idInvite 
    and   m.idMeeting = s.idMeeting
    """
    sql_vars = [user]
    my_query_results = db_conn.select2(sql, sql_vars)
    return my_query_results
    
def get_avg_score_per_meeting(user):
    db_conn = eamm.backend.database.MyDatabase()
    sql = """
    SELECT m.start_time, i.title, avg(s.survey_response_rating)
    FROM EAMM.Meeting as m INNER JOIN EAMM.Invite as i INNER JOIN EAMM.Survey as s
    WHERE m.meeting_chair=%s
    and   s.survey_response_rating != 0
    and   m.idInvite = i.idInvite 
    and   m.idMeeting = s.idMeeting
    group by m.idMeeting
    order by m.start_time desc
    """
    sql_vars = [user]
    my_query_results = db_conn.select2(sql, sql_vars)
    return my_query_results

def css(x):
    if x > 0 and x < 40:
        css = "red"
    elif x >= 40 and x < 65:
        css = "amber"
    else:
        css = "ggreen"
    
    return css