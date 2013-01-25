
#!/usr/bin/python

def test(**kwargs):
    var1 = kwargs.get("autocommit")
    print("var1 = %s" % var1)

test(autocommit="off")
    