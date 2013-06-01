#!/usr/bin/python

import eamm.backend.metrics 

def main():
    
    user = "richardarchbold@gmail.com"
    
    my_chart = eamm.backend.metrics.Chart()
    
    fhash = my_chart.file_hash(user)
    fname = "/tmp/" + fhash + ".png"
    
    my_chart.filename = fname
    
    img1 = my_chart.user_scores(user)

    print(img1)
    
if __name__ == '__main__':
    main()