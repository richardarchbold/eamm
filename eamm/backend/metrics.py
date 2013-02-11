# import various std libs
import cgitb; cgitb.enable(display=1)
from datetime import datetime
import md5
import time
import os

# import application libs
import eamm.backend.database

# plotting libs and basic setup
os.environ['MPLCONFIGDIR'] = "/var/www-graphs/"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



# setup basic logging config
import logging
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)


def get_tot_avg_score(user):
    db_conn = eamm.backend.database.MyDatabase()
    sql = """
    SELECT avg(s.survey_response_rating)
    FROM EAMM.Meeting as m 
        INNER JOIN EAMM.Invite as i 
        INNER JOIN EAMM.Survey as s
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
    FROM EAMM.Meeting as m 
        INNER JOIN EAMM.Invite as i 
        INNER JOIN EAMM.Survey as s
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


class Chart(object):
    def __init__(self):
        self.filename = None
        self.base_dir = "/home/richard/workspace/eamm/private/images/"
        self.img_dir  = "/eamm/private/images/"
        
    def user_scores(self, user):
        
        ####################################################################
        # we hash the filename of the image, to make it difficult for people
        # to guess filenames and view other peopls metrics.
        if not self.filename:
            hash_name = self.file_hash(user)
            self.filename = self.base_dir + hash_name + ".png"
            self.imgname  = self.img_dir  + hash_name + ".png"
        
        ###################################################
        # 0. Only (re)create file if it doesn't exist or is
        #    older than 2 mins.
        if self.is_fresh(self.filename):
            return self.imgname
        
        ###################################################
        # 1. get the data we want to plot
        db_conn = eamm.backend.database.MyDatabase()
    
        sql = """
        SELECT date(m.start_time) as date, i.title, 
               round(avg(s.survey_response_rating),1) as avg_rating
        FROM EAMM.Meeting as m 
          INNER JOIN EAMM.Invite as i 
          INNER JOIN EAMM.Survey as s
        WHERE m.meeting_chair=%s 
          and s.survey_response_rating != 0
          and m.idInvite = i.idInvite 
          and m.idMeeting = s.idMeeting
        group by m.idMeeting
        order by m.start_time
        """
        sql_vars = [user]
        rows = db_conn.select2(sql, sql_vars)
        
        ###################################################
        # 2. put the data in arrays
        g_dates = list()
        g_ratings = list()
    
        for row in rows:
            #print "date: %s, avg_rating: %s" % (row[0], row[2])
            g_dates.append(row[0])
            g_ratings.append(row[2])

        ###################################################
        # 2.1 get first and last dates in datetime format
        #print("type: %s, value: %s" % (type(g_dates[0]), g_dates[0]))
        datemin = datetime.strptime(g_dates[0].isoformat(),  '%Y-%m-%d')
        datemax = datetime.strptime(g_dates[-1].isoformat(), '%Y-%m-%d')
        
        ###################################################
        # 3. create a figure, create a chart in the figure
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid(True)
        
        ###################################################
        # 4. plot the data points
        line1 = ax.plot(g_dates, g_ratings)
        ax.set_ylim(top=100, bottom=0)
        ax.set_xlim(datemin, datemax)
    
        ###################################################
        # 5. plot the SLA line
        line2 = plt.axhline(y=65)      
        ax.legend()       
    
        ###################################################
        # 5. format the lines
        plt.setp(line1, color='b', linewidth=2.0, marker='.',
                 markeredgewidth=3.0, markersize=10.0,
                 label='Meeting Instance Score')
    
        plt.setp(line2, color='r', linewidth=2.0,
                 label='Meeting Score SLA line', )
        ax.legend()
    
        ###################################################
        # 6. format the X-axis
        ax.set_xlabel('Dates', fontsize=14, color='b')
        dateFmt = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(dateFmt)
        fig.autofmt_xdate(bottom=0.2, rotation=330, ha='left')
    
        ###################################################
        # 6. format the Y-axis
        ax.set_ylabel('Meeting Instance Score', fontsize=14, color='b')

        ###################################################
        # 7. render the plot
        title_text = "Meeting Survey Scores for %s" % user
        plt.title(title_text, color='green')
        plt.savefig(self.filename)
        
        return self.imgname
    
    ###########################################################################
    # method to turn a key word (eg a username into an md5 file hash'd URL
    def file_hash(self, name):
        m = md5.new()
        m.update(name)
        
        #hexdigest() - digest is returned as a string of length 32, containing 
        # only hexadecimal digits.
        hash_name = m.hexdigest()
        
        return hash_name
    
    
    ###########################################################################
    # we check to see if the file is fresh before attempting the reasonably
    # expensive process of regenerating it.
    def is_fresh(self, fname):
        logging.info("is_fresh fname = %s" % fname)
        
        try:
            stat=os.stat(fname)
        except Exception as e:
            logging.info("Could not stat %s, error msg - %s" % (fname, str(e)))
            return False
        
        two_minutes_ago = time.time() - 120
        mtime=stat.st_mtime
        logging.info("%s < %s" % (mtime, two_minutes_ago))
        if mtime < two_minutes_ago:
            logging.info("%s is fresh enough, no need to regenerate" % fname)
            return True
        else:
            return False
        