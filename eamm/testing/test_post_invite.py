#!/usr/bin/python

import urllib, urllib2

def main():
    
    username = 'test'
    password = 'test-pass'
    url = 'http://127.0.0.1/eamm/private/add_meeting_invite.py'
    
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

    raw_params = {
                  'step': 'step4',
                  'purpose': "test purpose",
                  'justification': "test justification",
                  'template': "2",
                  'agenda': "test agenda",
                  'title': "test title",
                  'start_date': "2014-01-01",
                  'start_time': "20:00",
                  'duration': "40",
                  'recurring': "none",
                  'venue': "test venue",
                  'requester': "requester@test.com",
                  'invitees': "<p>c@c.com</p>"
                  }
    
    params = urllib.urlencode(raw_params)

    request = urllib2.Request(url, params)
    page = urllib2.urlopen(request)
    print page.read()
    
    
if __name__ == '__main__':
    main()