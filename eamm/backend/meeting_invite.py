import logging

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInvite(object):
    
    def __init__(self, arg1=None):
        
        if arg1 == None:
            # no arguments passed
            pass
        elif type(arg1) is int:
            # arg1 is an int, likely an existing id_meeting_invite
            pass
        elif arg1.getvalue('purpose'):
            # arg1 is a form object instance.
            #logging.info("MeetingTemplate() was passed a form as an object")
            form = arg1
            
            # error back to the calling class if we can't load the form.
            if self.__load_form(form) == False:
                return False
    
    # add a row to the invite table.
    # add the corresponding row(s) to the meeting table.
    #
    #   row(s) because if it is a recurring meeting there will be multiple rows in
    #   the meeting table for the single row in the invite table.
    #
    def add(self):
        # sql to add to the 
        
        pass
    
    # initialize all key class attributes from form data.        
    def __load_form(self, form):
        
        # check to make sure all fields have stuff in them.
        if not all((form.getvalue('purpose'), form.getvalue('justification'), 
                    form.getvalue('template'), form.getvalue('agenda'), 
                    form.getvalue('title'), form.getvalue('start_date'),
                    form.getvalue('start_time'), form.getvalue('recurring'),
                    form.getvalue('end_date'), form.getvalue('venue'),
                    form.getvalue('requester'), form.getvalue('invitees'))):
            return False
        
        self.purpose = form.getvalue('purpose')              # wysiwyg html string
        self.justification = form.getvalue('justification')  # wysiwyg html string
        self.id_template = form.getvalue('template')         # integer
        self.agenda = form.getvalue('agenda')                # wysiwyg html string
        self.title = form.getvalue('title')                  # string
        self.start_date = form.getvalue('start_date')        # yyyy-mm-dd string
        self.start_time = form.getvalue('start_time')        # hh:mm 24 hr strong 
        self.recurring = form.getvalue('recurring')          # string
        self.end_date = form.getvalue('end_date')            # yyyy-mm-dd string
        self.venue = form.getvalue('venue')                  # string
        self.requester = form.getvalue('requester')          # you@example.com string
        self.invitees = form.getvalue('invitees')            # wysiwyg html string    
        
       
    
