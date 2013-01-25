#!/usr/bin/python

def test_var_args(aaa, *bbb):
    print "formal arg:", aaa
    for arg in bbb:
        print "another arg:", arg

test_var_args(1, "two", 3)

