#!/usr/bin/python

import re

def main():        
    # if everything worked right, we'll have something like:
    #
    #<p>richard@a.com</p>
    #<p>frances@b.com</p>
    #
    
    my_txt = """<p>richard@a.a..com</p>
    <p>frances@b.com</p>
    <p>sdfsfdsf@sdfkasfd.com&"""
        
    lines = my_txt.split('\n')
    
    i=0

    for line in lines:
        
        # get rid of bracketing white spaces and print the line
        line = line.strip()
        print("line: %s" % line)
            
        # get rid of HTML tags with a non-greedy search and replace.
        line = re.sub("<.*?>","", line)
        print("line: %s" % line)
        
        if re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$', line):
            print("line is an email address: %s\n\n" % line)
            lines[i] = line
        else:
            print("line is NOT an emaila ddress: %s\n\n" % line)
            del lines[i]
            
        i+=1
        
    print(tuple(lines))
if __name__ == '__main__':
    main()