from app import *
import time
import datetime


def getCurrentSemester():
    """
        查询当前的学期
        @:return 这学期开始的那一天
    """
    this_year = datetime.date.today().year
    today = datetime.date.today()
    this_semester_start = ""
    if today <= datetime.date(this_year, 9, 1):
        if today <= datetime.date(this_year, 2, 10):
            this_semester_start = str(this_year - 1) + "-09-01"
        else:
            this_semester_start = str(this_year) + "-02-10"
    else:
        this_semester_start = str(this_year) + "-09-01"
    return datetime.datetime.strptime(this_semester_start, '%Y-%m-%d')


def getWeekday(date):
    """
        查询这天是星期几
        @:param 这一天的年月日时间
        @:return 周几，比如1 就是周一
    """
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    return d.weekday() + 1


def getCurrentWeek():
    """
        查询当前的星期一的日期是几号
        @:return 返回当前星期一的日期
    """
    monday= datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    # datatime类型转格式字符串
    monday = monday.strftime("%Y-%m-%d")
    return monday


def getLastWeek():
    """
        查询上一周周一的日期是几号
        @:return 返回上一个星期的日期
    """
    monday = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    monday -= one_day
    while monday.weekday() != 0:
        monday -= one_day
    # datatime类型转格式字符串
    monday = monday.strftime("%Y-%m-%d")
    return monday


def getCurrentMouth():
    """
        查询这个月月初是几号
        @:return 返回这个月月初的日期
    """
    first = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
    # datatime类型转格式字符串
    first = first.strftime("%Y-%m-%d")
    return first


def getCurrentTime():
    """
        查询当前时间戳
        @:return 返回当前的时间戳
    """
    return time.time()


def getCurrentSchoolMemberSemester():
    """
        获取当前时间在校成员的最高年级
        比如2019年9月以前就包括了2016届成员
        2019年9月以后最高年级成员就成了2017届了
        :return: 返回最高年级数，比如2017
    """
    thisYear = datetime.datetime.now().year
    mouth = datetime.datetime.now().month
    if mouth >= 9:
        return thisYear-2
    else:
        return thisYear-3


def getTwoTimeHaveWeek(start_time,end_time):
    if type(start_time) == str:
        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    if type(end_time) == str:
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    days = end_time-start_time
    week = 1+int(days.days/6)
    return week


def getCurrentGrade():
    return getCurrentSchoolMemberSemester()+1,getCurrentSchoolMemberSemester()+2

if __name__ == '__main__':
    print(getTwoTimeHaveWeek(getCurrentSemester(),datetime.datetime.today()))

