#!/usr/bin/python

"""A one line summary of the module or script, terminated by a period.

Leave one blank line. The rest of this __doc__ string should contain an
overall description of the module or script.  Optionally, it may also
contain a brief description of exported classes and functions.

    ClassFoo: One line summary.
    functionBar(): One line summary.

Source:http://github/richardarchbold/eamm.git
Created: 9 Jan 2013
"""
__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

import eamm.meeting_template

def main():
    my_meeting_template = eamm.meeting_template.MeetingTemplate() 
    all_templates = my_meeting_template.get_all()
    
    #my_type = type(all_templates)
    #print("type of all_templates is %s", my_type)
    
    for count in range(len(all_templates)):
            title = all_templates[count][0]
            description = all_templates[count][1]
            purpose = all_templates[count][2]
            print("title: %s" % title)
            print("desc: %s" % description)
            print("purpose: %s \n\n" % purpose)

if __name__ == '__main__':
    main()