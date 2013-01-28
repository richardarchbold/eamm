#!/usr/bin/python

def main():
    sql = """
    INSERT into Invite (start_date, duration, end_date, recurring, invite_status, title, 
                        purpose, background_reading, agenda, requester_email_addr, venue, 
                        idMeetingTemplate) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    print(sql)

if __name__ == '__main__':
    main() 
