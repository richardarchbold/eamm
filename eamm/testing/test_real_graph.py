#!/usr/bin/python

# script to display a graph of my avg meeting scores.

# plotting libs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# other libs
import eamm.backend.database

def main():
    
    ###################################################
    # 1. get the data we want to plot
    db_conn = eamm.backend.database.MyDatabase()
    
    sql = """
    SELECT date(m.start_time) as date, i.title, round(avg(s.survey_response_rating),1) as avg_rating
    FROM EAMM.Meeting as m 
        INNER JOIN EAMM.Invite as i 
        INNER JOIN EAMM.Survey as s
    WHERE m.meeting_chair='richardarchbold@gmail.com' 
        and   s.survey_response_rating != 0
        and   m.idInvite = i.idInvite 
        and   m.idMeeting = s.idMeeting
        group by m.idMeeting
    order by m.start_time
    """
    rows = db_conn.select(sql)
    
    ###################################################
    # 2. put the data in arrays
    g_dates = list()
    g_ratings = list()
    
    for row in rows:
        print "date: %s, avg_rating: %s" % (row[0], row[2])
        g_dates.append(row[0])
        g_ratings.append(row[2])

    ###################################################
    # 2.1 get first and last dates in datetime format
    print("type: %s, value: %s" % (type(g_dates[0]), g_dates[0]))
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
    user = "richardarchbold@gmail.com"
    title_text = "Meeting Survey Scores for %s" % user
    plt.title(title_text, color='green')
    plt.show()
    
    
if __name__ == '__main__':
    main()