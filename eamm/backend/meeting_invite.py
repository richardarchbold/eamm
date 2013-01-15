import logging

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInvite(object):
    
    def __init__(self, argg1=None):
        
        if argg1 == None:
            # no arguments passed
            pass
        elif type(argg1) is int:
            # arg1 is an int, likely an existing id_meeting_invite
            pass
        elif argg1.getvalue('purpose'):
            # arg1 is a form object instance.
            logging.info("MeetingTemplate() was passed a form as an object")
    
        # purpose = form.getvalue('purpose')              # wysiwyg html string
        # justification = form.getvalue('justification')  # wysiwyg html string
        # id_template = form.getvalue('template')         # integer
        # agenda = form.getvalue('agenda')                # wysiwyg html string
        # title = form.getvalue('title')                  # string
        # start_date = form.getvalue('start_date')        # yyyy-mm-dd string
        # start_time = form.getvalue('start_time')        # hh:mm 24 hr strong 
        # recurring = form.getvalue('recurring')          # string
        # end_date = form.getvalue('end_date')            # yyyy-mm-dd string
        # venue = form.getvalue('venue')                  # string
        # requester = form.getvalue('requester')          # you@example.com string
        # invitees = form.getvalue('invitees')            # wysiwyg html string            
        