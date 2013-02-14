#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.base_webpage
import eamm.backend.metrics

import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    user = os.environ['REMOTE_USER']
    
    this_webpage = eamm.frontend.base_webpage.WebPage()
    this_webpage.set_title("Meeting Metrics for %s" % user)
        
    tot_avg_score         = eamm.backend.metrics.get_tot_avg_score(user)
    avg_score_per_meeting = eamm.backend.metrics.get_avg_score_per_meeting(user)
    
    my_chart = eamm.backend.metrics.Chart()
    chart1 = my_chart.user_scores(user) 
    
    img1 = """<img src="%s"/>""" % chart1
    
    num_meetings = len(avg_score_per_meeting)
    
    if (num_meetings == 0):
        msg  = "No metrics exist for %s as no surveys have" % user
        msg += "been submitted for this user yet"
        tbl = this_webpage.error_table(msg)
        this_webpage.add_to_body(tbl)
    else:
        rowspan = 4 + num_meetings
        t_css = eamm.backend.metrics.css(int(tot_avg_score[0][0]))
        html = """ 
    
        %s
    
        <table>
         <tr>
            <td class="col1" rowspan="%s">User Meeting Metrics</td>
            <td class="col2_top" colspan="3"><b>Scope: All Meetings</b></td>
          </tr>
          <tr>
           <td class="sub_col_1a" colspan="2">
           Average Rating (all meetings, all questions)</td>
            <td class="%s">%s</td>
          </tr>
          <tr>
            <td class="col2_top" colspan="3">
            <b>Scope: Individual Meetings</b></td>
          </tr>
         <tr>
            <td class="col2_top"><b><i>Date</i></b></td>
            <td class="col2_top"><b><i>Title</i></b></td>
           <td class="col2_top""><b><i>Score</i></b></td>
        """ % (img1, rowspan, t_css, int(tot_avg_score[0][0]))
    
        for row in avg_score_per_meeting:
            score = int(row[2])
            css = eamm.backend.metrics.css(score)
            
            # row is start_time, title, avg_rating
            html += """
            <tr>
              <td class="sub_col_1a">%s</td>
              <td class="sub_col_1a">%s</td>
              <td class="%s">%s</td>
            </tr>
            """ % (row[0], row[1], css, score)
    
        html += """<tr><td class="header" colspan="4">%s
        </td></tr>""" % this_webpage.home_button
        html += "</table>"
        this_webpage.add_to_body(html)
        
    this_webpage.render()
    
    
    
if __name__ == '__main__':
    main()