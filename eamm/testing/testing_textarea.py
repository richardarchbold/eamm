#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

import eamm.frontend.base_webpage

def main():
    page = eamm.frontend.base_webpage.WebPage()
    page.set_title("test")
    page.add_to_body("test")
    page.render()

if __name__ == '__main__':
    main()