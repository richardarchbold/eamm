#!/usr/bin/python

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.meeting_invite_webpage
import cgi
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)
logging.info("======")

def main():

    this_webpage = eamm.frontend.meeting_invite_webpage.MeetingInviteWebPage()
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.add_meeting_invite_step_1()
    elif os.environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage()
        logging.info("form type: %s" % type(form))
        
        if not form.getvalue('step'):
            this_webpage.set_title("Add Meeting Invite :: Error")
            this_webpage.error_table("No form step set")
        else:
            step = form.getvalue('step')
            logging.info("step: %s" % step)
            
            if step == 'step1':
                this_webpage.add_meeting_invite_step_2(form)
            elif step == 'step2':
                this_webpage.add_meeting_invite_step_3(form)
            elif step == 'step3':
                this_webpage.add_meeting_invite_step_4(form)
            elif step == 'step4':
                this_webpage.add_meeting_invite_step_5(form)

    this_webpage.render()
       
if __name__ == '__main__':
    main()