import csv
import calendar
from time import gmtime, strftime, localtime, strptime


###################
# TODO 法定节假日
# TODO 闰年
# TODO 工作日判断
# TODO 调休
###################
TIME_COL = 3
CSV_HEADER = "出勤时间"
YEAR = 2014
MONTH = 12

class WorkingTime:
    def __init__(self, year, month, day):
        self.begin_time = None
        self.end_time = None
        self._year = year
        self._month = month
        self._day = day

    def is_workday(self):
        return self.end_time.tm_wday < 5

    def is_overtime(self, leaving_time):
        if self.is_workday():
            if leaving_time >= 12 + 7.5:
                return True
            else:
                return False
        else:
            return True

    def count(self):
        if self.begin_time is None or self.end_time is None or self.begin_time == self.end_time :
            return None
        mbs = self.begin_time.tm_hour + 0.5 if self.begin_time.tm_min < 30 else self.begin_time.tm_hour + 1
        mbe = self.end_time.tm_hour + 0.5 if self.end_time.tm_min > 30 else self.end_time.tm_hour
        return self.is_overtime(mbe)
        # return mbe - mbs

sample_time = "2014-12-1, 9:02"

# 获得当月天数
days_of_month = calendar.monthrange(YEAR, MONTH)[1]
# 构建本月时间表
working_time_in_month = [WorkingTime(YEAR, MONTH, i)
                         for i in range(0, days_of_month + 1)]

with open('/tmp/t.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        if row[3] != CSV_HEADER:
            t = strptime(row[TIME_COL], "%Y-%m-%d %H:%M")
            if (t.tm_year != YEAR or t.tm_mon != MONTH):
                continue

            working_time = working_time_in_month[t.tm_mday]
            working_time.begin_time = t if working_time.begin_time is None \
                                      else min(working_time.begin_time, t)
            working_time.end_time = t if working_time.end_time is None \
                                      else max(working_time.end_time, t)

            # working_time.begin_time = t
            # print (strptime(row[TIME_COL], "%Y-%m-%d %H:%M"))
            # print (strptime(row[TIME_COL], "%Y-%m-%d %H:%M") <
            # localtime())
for wk in working_time_in_month[1:]:
    print (wk._year, wk._month, wk._day, "加班" if wk.count() else "无加班")

print (working_time_in_month[1].begin_time)
# print (working_time_in_month[1].end_time)
# print (working_time_in_month[1].end_time - working_time_in_month[1].begin_time)
