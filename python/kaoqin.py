import csv
import json
import calendar
from datetime import date
from time import gmtime, strftime, localtime, strptime

# Global Settings.
# 会在载入配置时全部重新生成, 可以全部删除, 留此仅作为说明作用
SPECIFIC_WORKDAY = {}
SPECIFIC_HOLIDAY = {}
LEAVE_HOUR = 18
ARRIVE_HOUR = 9
MIN_OVERTIME = 1
fields_functions = {
    "timestamp": lambda row, time_col=3: row[time_col],
    "name": lambda row, name_col=2: row[name_col]
}
is_skipped_row = lambda row: not row or row[3] == '出勤时间'
time_formatter_function = lambda time_str: strptime(time_str, "%Y-%m-%d %H:%M")

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

class TimeSheetDailyReport:
    def __init__(self):
        self.late = False
        self.late_time_hours = 0
        self.early_leave = False
        self.early_leave_hours = 0
        self.overtime = False
        self.overtime_hours = 0
        
        self.absent = False
        self.late_in_ten_minutes = False
        self.data_missed = False

    def to_json(self):
        json_obj = {
            "late": self.late,
            "late_time_hours":self.late_time_hours,
            "early_leave":self.early_leave,
            "early_leave_hours":self.early_leave_hours,
            "overtime":self.overtime,
            "overtime_hours":self.overtime_hours,
            "absent":self.absent,
            "late_in_ten_minutes":self.late_in_ten_minutes,
            "data_missed":self.data_missed
            }
        return json.dumps(json_obj, sort_keys = True)

class TimeSheetMonthlyReport:
    def __init__(self):
        self.late_in_ten_minutes_count = 0
        self.total_overtime = 0
        self.total_leaving_time = 0
        self.total_absent = 0
        self.data_missed_count = 0

    def to_json(self):
        json_obj = {
            "late_in_ten_minutes_count":self.late_in_ten_minutes_count,
            "total_leaving_time":self.total_leaving_time,
            "total_overtime":self.total_overtime,
            "total_absent":self.total_absent,
            "data_missed_count":self.data_missed_count
            }
        return json.dumps(json_obj, sort_keys = True)

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


def csv_row_reader(row, fields, time_formatter_function, wts):
    time_str = fields["timestamp"](row)
    if time_str:
        timestamp = time_formatter_function(time_str)
        wts.append_timestamp(timestamp)
    else:
        # We really can't handle this situation.
        raise FileFormatError("We can't find the timestamp field. May be a wrong file")


def parse_csv(file_name, fields_functions, continue_function):
    wts = WorkingTimeSchedule(2015)
    with open(file_name, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if is_skipped_row(row):
                continue
            csv_row_reader(row,
                           fields_functions,
                           time_formatter_function,

                           wts)
    return wts


def generate_monthly_report(month_time_sheet_report):
    monthly_report = month_time_sheet_report[0]
    for day, daily_report in enumerate(month_time_sheet_report):
        if day == 0: continue
        if daily_report.late_in_ten_minutes:
            monthly_report.late_in_ten_minutes_count += 1
        if daily_report.absent:
            monthly_report.total_leaving_time += 8
            monthly_report.total_absent += 1
        if daily_report.data_missed:
            monthly_report.data_missed_count += 1
        monthly_report.total_leaving_time += daily_report.early_leave_hours
        monthly_report.total_leaving_time += daily_report.late_time_hours
        monthly_report.total_overtime += daily_report.overtime_hours
    return monthly_report

def holiday_daily_report(daily_working_time, daily_report):
    overtime = daily_working_time.end_hour - daily_working_time.begin_hour
    if overtime > 0:
        daily_report.overtime = True
        daily_report.overtime_hours = overtime


def workday_daily_report(daily_working_time, daily_report):
    late = daily_working_time.begin_hour - ARRIVE_HOUR
    early_leave = LEAVE_HOUR - daily_working_time.end_hour
    overtime = daily_working_time.end_hour - (LEAVE_HOUR + 0.5)
    if daily_working_time.begin_hour == 0:
        daily_report.absent = True
    else:
        if late > 0:
            daily_report.late = True
            daily_report.late_time_hours = late
            if daily_working_time.begin_time.tm_hour == 9 and daily_working_time.begin_time.tm_min <=10:
                daily_report.late_in_ten_minutes = True
        if early_leave > 0:
            daily_report.early_leave = True
            daily_report.early_leave_hours = early_leave
        if overtime >= MIN_OVERTIME:
            daily_report.overtime = True
            daily_report.overtime_hours = overtime


def generate_daily_report(daily_working_time, daily_report, spec_workday, spec_holiday):
    if (daily_working_time.end_hour - daily_working_time.begin_hour < 0):
        daily_report.data_missed = True
        return
    
    if (daily_working_time.is_weekend() or daily_working_time._day in spec_holiday) and (daily_working_time._day not in spec_workday):
        holiday_daily_report(daily_working_time, daily_report)
    else:
        workday_daily_report(daily_working_time, daily_report)

def generate_time_sheet_report(wts):
    time_sheet_report = {}
    for ynm, v in wts._working_time_pairs.items():
        spec_workday = SPECIFIC_WORKDAY[ynm] if ynm in SPECIFIC_WORKDAY else []
        spec_holiday = SPECIFIC_HOLIDAY[ynm] if ynm in SPECIFIC_HOLIDAY else []

        time_sheet_report[ynm] = [TimeSheetDailyReport() for i in range(len(v))]
        time_sheet_report[ynm][0] = TimeSheetMonthlyReport()
        [generate_daily_report(working_time,
                               time_sheet_report[ynm][day],
                               spec_workday,
                               spec_holiday) for day, working_time in enumerate(v) if day != 0]
        generate_monthly_report(time_sheet_report[ynm])
    return time_sheet_report


def load_config(json_config):
    global ARRIVE_HOUR, LEAVE_HOUR, MIN_OVERTIME, SPECIFIC_WORKDAY, SPECIFIC_HOLIDAY
    global is_skipped_row, fields_functions, time_formatter_function

    with open(json_config) as json_file:
        json_obj = json.load(json_file)
        ARRIVE_HOUR = json_obj["arrive_hour"] if "arrive_hour" in json_obj else 9
        LEAVE_HOUR = json_obj["leave_hour"] if "leave_hour" in json_obj else 18
        MIN_OVERTIME = json_obj["min_overtime"] if "min_overtime" in json_obj else 1
        SPECIFIC_WORKDAY = json_obj["specific_workday"] if "specific_workday" in json_obj else {}
        SPECIFIC_HOLIDAY = json_obj["specific_holiday"] if "specific_holiday" in json_obj else {}
        is_skipped_row = eval(json_obj["is_skipped_row"]) if "is_skipped_row" in json_obj else lambda row: not row or row[3] == '出勤时间'
        if "fields_functions" in json_obj:
            fields_functions = eval(json_obj["fields_functions"])
        else:
            fields_functions = {
                "timestamp": lambda row, time_col=3: row[time_col],
                "name": lambda row, name_col=2: row[name_col] }
        if "time_formatter" in json_obj:
            time_formatter_function = eval(json_obj["time_formatter"])
        else:
            time_formatter_function = lambda time_str: strptime(time_str, "%Y-%m-%d %H:%M")

def output_plain_text_report(time_sheet_report):
    for ynm, reports in time_sheet_report.items():
        print (ynm)
        print ('=====================================================================')
        mr = reports[0]
        print ("本月共计加班{0}小时, 请假调休等共计{1}小时, 其中有{2}次为10分钟以内迟到, 按照0.5小时计入, 全天请假{3}次(也有可能为数据丢失), 另有{4}天数据不完整无法计算, 不计入以上统计.".format(
            mr.total_overtime,
            mr.total_leaving_time,
            mr.late_in_ten_minutes_count,
            mr.total_absent,
            mr.data_missed_count))
        print ("以下为详细信息,")

        for day, report in enumerate(reports):
            if day == 0: continue
            output_text = "本月第{0}日:\t".format(day)
            if report.late:
                output_text += "迟到{0}小时".format(report.late_time_hours)
                if report.late_in_ten_minutes:
                    output_text += "(为10分钟以内迟到). "
                else:
                    output_text += ". "
            if report.early_leave:
                output_text += "早退{0}小时. ".format(report.early_leave_hours)
            if report.overtime:
                output_text +="加班{0}小时. ".format(report.overtime_hours)
            if report.absent:
                output_text +="全天请假, 或者无打卡记录. "
            if report.data_missed:
                output_text +="数据不完整. "
            if output_text == "本月第{0}日:\t".format(day):
                output_text += "..."
            print(output_text)

import sys
cfg_json = sys.argv[1]
csv_file = sys.argv[2]
load_config(cfg_json)
wts = parse_csv(csv_file, fields_functions, is_skipped_row)
wts.discretize()
report = generate_time_sheet_report(wts)
output_plain_text_report(report)


