# -*- coding: utf-8 -*-
#!/bin/python


import datetime


t2 = datetime.date(2013,10,23)
t1 = datetime.date.today()

delta_days = (t2 - t1).days

print "亲，到截止时间还有" ,delta_days, "天思密达"
