import csv
import calendar
from datetime import date
from time import gmtime, strftime, localtime, strptime


class WorkingTime:
    def __init__(self, year, month, day):
        self.begin_time = None
        self.end_time = None
        self.begin_hour = 0
        self.end_hour = 0
        self._year = year
        self._month = month
        self._day = day

        if day != 0:
            self._wday = date(year, month, day).weekday()

    def update(self, t):
        self.begin_time = t if self.begin_time is None else min(self.begin_time, t)
        self.end_time = t if self.end_time is None else max(self.end_time, t)

    def is_weekend(self):
        return self._wday > 4

    def discretize(self):
        if self.begin_time is not None:
            self.begin_hour = self.begin_time.tm_hour+0.5 if self.begin_time.tm_min < 30 else self.begin_time.tm_hour + 1
        if self.end_time is not None:
            self.end_hour = self.end_time.tm_hour + 0.5 if self.end_time.tm_min > 30 else self.end_time.tm_hour


class FileFormatError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MonthRange:
    def __init__(self, year):
        self._cache = dict([(year*100+m, calendar.monthrange(year, m)[1]) for m in range(1, 13)])

    def get(self, year, month):
        hashcode = year*100+month
        if hashcode not in self._cache:
            self._cache[hashcode] = calendar.monthrange(year, month)[1]
        return self._cache[hashcode]


class WorkingTimeSchedule:
    def __init__(self, year):
        self._working_time_pairs = {}
        self._month_range = MonthRange(year)

    def unpack(self, t):
        return t.tm_year, t.tm_mon

    def append_timestamp(self, timestamp):
        year, month = self.unpack(timestamp)
        hashcode = year*100+month
        if hashcode not in self._working_time_pairs:
            self.append_whole_month_schedule(year, month)
        self.update_working_time(hashcode, timestamp)

    def append_whole_month_schedule(self, year, month):
        mr = self._month_range.get(year, month)
        self._working_time_pairs[year*100+month] = [
            WorkingTime(year, month, day) for day in range(mr+1)]

    def update_working_time(self, year_n_month, timestamp):
        day = timestamp.tm_mday
        self._working_time_pairs[year_n_month][day].update(timestamp)

    def discretize(self):
        for k, v in self._working_time_pairs.items():
            for wt in v:
                wt.discretize()

    def print_self(self):
        for k in self._working_time_pairs:
            print (k)
            for wt in self._working_time_pairs[k]:
                print (wt.begin_time)
                print (wt.end_time)
                print ("------------------------------------------")


def csv_row_reader(row, fields, time_formatter_function, wts):
    time_str = fields["timestamp"](row)
    if time_str:
        timestamp = time_formatter_function(time_str)
        wts.append_timestamp(timestamp)
    else:
        # We really can't handle this situation.
        raise FileFormatError("We can't find the timestamp field. May be a wrong file")

fields_functions = {
    "timestamp": lambda row, time_col=3: row[time_col],
    "name": lambda row, name_col=2: row[name_col]
}
is_skipped_row = lambda row: not row or row[3] == "出勤时间"


def parse_csv(file_name, fields_functions, continue_function):
    wts = WorkingTimeSchedule(2015)
    with open(file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if is_skipped_row(row):
                continue
            csv_row_reader(row,
                           fields_functions,
                           lambda time_str: strptime(time_str, "%Y-%m-%d %H:%M"),
                           wts)
    return wts

wts = parse_csv("/tmp/t.csv", fields_functions, is_skipped_row)
wts.discretize()

# TODO may be list of list to store the whole year's data.
SPECIFIC_WORKDAY = {
    201504: [1, 2, 3, 4]
}
SPECIFIC_HOLIDAY = {
    201504: [1, 10, 11]
}

LEAVE_HOUR = 18
ARRIVE_HOUR = 9

for ynm, v in wts._working_time_pairs.items():
    print (ynm, ":")
    spec_workday = SPECIFIC_WORKDAY[ynm] if ynm in SPECIFIC_WORKDAY else []
    spec_holiday = SPECIFIC_HOLIDAY[ynm] if ynm in SPECIFIC_HOLIDAY else []

    for wt in v[1:]:
        print (wt._day, end=' ')
        if (wt.end_hour - wt.begin_hour < 0):
            print ('\t缺少打卡或者数据有误')
            continue
        if (wt.is_weekend() or wt._day in spec_holiday) and (wt._day not in spec_workday):
            overtime = wt.end_hour - wt.begin_hour
            if overtime > 0:
                print ("\t加班时间", overtime)
        else:
            late = wt.begin_hour - ARRIVE_HOUR
            early_leave = LEAVE_HOUR - wt.end_hour
            overtime = wt.end_hour - (LEAVE_HOUR + 0.5)
            if wt.begin_hour == 0:
                print ("\t当天请假或无打卡数据")
            else:
                if late > 0:
                    print ("\t迟到时间", late)
                    if wt.begin_time.tm_hour == 9 and wt.begin_time.tm_min <=10:
                        print ("\t十分钟以内")
                if early_leave > 0:
                    print ("\t早退时间", early_leave)
                if overtime >= 1:
                    print ("\t加班", overtime)


print ('Aha')
