#!/usr/bin/python

import eamm.backend.survey

def main():
    ques = eamm.backend.survey.get_questions(1)
    print(ques[0])

if __name__ == '__main__':
    main()