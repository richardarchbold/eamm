#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm")

import eamm.backend.meeting_invite
import eamm.backend.meeting


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders
from datetime import datetime

import eamm.backend.metrics

###################################
# eamm variables
id_invite  = 40
my_invite  = eamm.backend.meeting_invite.MeetingInvite(id_invite)
id_meeting = 141
my_meeting = eamm.backend.meeting.Meeting(id_meeting)
#
###################################

###################################
# static variables
CRLF      = "\r\n"
login     = "eamm.project@gmail.com"
password  = "ditboltonstreet"
#
###################################

#attendees = ["richardarchbold@gmail.com"]
attendees = my_invite.invitees_list

#organizer = "ORGANIZER;CN=organiser:mailto:richardarchbold1@eircom.net"
organizer = "ORGANIZER;CN=organiser:mailto:%s" % my_invite.requester

# fro does not need to be (a) real or (b) a gmail account
#fro = "RichO <richardarchbold@eircom.net>"
fro = "%s <%s>" % (my_invite.requester, my_invite.requester)

# summary is like that title/subject line
#summary = "testing summary "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF
summary = "%s %s" % (my_invite.title, CRLF)

# description is like the purpose
#description = "DESCRIPTION: test invitation from test_email_invite.py"+CRLF
description = "DESCRIPTION: %s %s" % (my_invite.purpose, CRLF) 

loc = my_invite.venue

###################################
# dynamic variables

#dt_start = datetime.strptime(my_invite.start_date, "%Y-%m-%d %H:%M:%S")
dt_start = my_meeting.start_datetime
#dt_end   = datetime.strptime(my_invite.end_date, "%Y-%m-%d %H:%M:%S")
dt_end   = my_meeting.end_datetime
duration = my_invite.duration

rule = ""
if my_invite.recurring != 'none':
    until = my_invite.end_date
    dt_until = until.strftime("%Y%m%dT%H%M%SZ")
    wk_day_idx = ((dt_start.day + 6) // 7)
    wk_day = dt_start.strftime('%a').upper()[:2]
    
    if   my_invite.recurring == 'daily':
        rule = "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR;UNTIL=%s" % dt_until
    elif my_invite.recurring == 'weekly':
        # RRULE:FREQ=WEEKLY;UNTIL=20130312T123000Z
        rule = "RRULE:FREQ=WEEKLY;UNTIL=%s" % dt_until
        
    elif my_invite.recurring == 'monthly':
        # RRULE:FREQ=MONTHLY;UNTIL=19971224T000000Z;BYDAY=1FR
        rule = "RRULE:FREQ=MONTHLY;UNTIL=%s;BYDAY=%s%s" % (dt_until, 
                                                           wk_day_idx, 
                                                           wk_day)
    elif my_invite.recurring == 'quarterly':
        rule = "RRULE:FREQ=MONTHLY;INTERVAL=3;UNTIL=%s;BYDAY=%s%s" % (dt_until, 
                                                                    wk_day_idx, 
                                                                    wk_day)
    rule += CRLF
    print rule

dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
dtstart = dt_start.strftime("%Y%m%dT%H%M%SZ")
dtend   = dt_end.strftime("%Y%m%dT%H%M%SZ")

uuid_str = "idMeeting:%s;requester:%s" % (my_invite.id_invite, 
                                          my_invite.requester) 

# re-using the file_hash function in Chart() object.
tmp = eamm.backend.metrics.Chart()
uuid = tmp.file_hash(uuid_str)

#
###################################

attendee = ""
for att in attendees:
    attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;" \
              + "ROLE=REQ-PARTICIPANT;"       \
              + "PARTSTAT=ACCEPTED;"          \
              + "RSVP=TRUE;"                  \
              + "CN="+att+";"                 \
              + "X-NUM-GUESTS=0:"             \
              + "mailto:"+att+CRLF
              
    print "******\nDEBUG:\n******\n%s" % attendee

ical = "BEGIN:VCALENDAR"+CRLF        \
     + "PRODID:pyICSParser"+CRLF     \
     + "VERSION:2.0"+CRLF            \
     + "CALSCALE:GREGORIAN"+CRLF     \
     + "METHOD:REQUEST"+CRLF         \
     + "BEGIN:VEVENT"+CRLF           \
     + "DTSTART:"+dtstart+CRLF       \
     + "DTEND:"+dtend+CRLF           \
     + "DTSTAMP:"+dtstamp+CRLF       \
     + rule                          \
     + organizer+CRLF                \
     + "UID:"+uuid+CRLF              \
     + attendee                      \
     + "CREATED:"+dtstamp+CRLF       \
     + description                   \
     + "LAST-MODIFIED:"+dtstamp+CRLF \
     + "LOCATION:"+loc+CRLF          \
     + "SEQUENCE:0"+CRLF             \
     + "STATUS:CONFIRMED"+CRLF       \
     + "SUMMARY:"+summary            \
     + "TRANSP:OPAQUE"+CRLF          \
     + "RRULE:FREQ=WEEKLY;WKST=MO;"+CRLF \
     + "EXRULE:FREQ=WEEKLY;BYDAY=SA,SU"+CRLF \
     + "END:VEVENT"+CRLF             \
     + "END:VCALENDAR"+CRLF

print "******\nDEBUG:\n******\n%s" % ical

#exit()

eml_body = "Meeting Title: %s <br>" % my_invite.title \
         + "Meeting Purpose: %s " % my_invite.purpose
eml_body_bin = "This is the email body in binary - two steps"

msg = MIMEMultipart('mixed')
msg['Reply-To']=fro
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = "Meeting invite: "+ summary
msg['From'] = fro
msg['To'] = ",".join(attendees)

part_email = MIMEText(eml_body,"html")
part_cal = MIMEText(ical,'calendar;method=REQUEST')

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
ical_atch.set_payload(ical)
Encoders.encode_base64(ical_atch)
ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

eml_atch = MIMEBase('text/plain','')
Encoders.encode_base64(eml_atch)
eml_atch.add_header('Content-Transfer-Encoding', "")

msgAlternative.attach(part_email)
msgAlternative.attach(part_cal)

mailServer = smtplib.SMTP('smtp.gmail.com', 587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login(login, password)
mailServer.sendmail(fro, attendees, msg.as_string())
mailServer.close()