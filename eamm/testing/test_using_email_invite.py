#!/usr/bin/python

import eamm.backend.email_invite

def main():
    id_invite  = 40
    #id_meeting = 141
    
    my_email_invite = eamm.backend.email_invite.EmailInvite(id_invite) 
 
    my_email_invite.send()
    
if __name__ == '__main__':
    main()