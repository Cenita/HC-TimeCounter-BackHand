from app import *
import datetime


def get_current_semester():
    this_year = datetime.date.today().year
    today = datetime.date.today()
    this_semester_start = ""
    if today<=datetime.date(this_year,9,1):
        if today<=datetime.date(this_year,2,10):
            this_semester_start = str(this_year-1)+"-09-01"
        else:
            this_semester_start = str(this_year)+"-02-10"
    else:
        this_semester_start = str(this_year)+"-09-01"
    return this_semester_start





def get_weekday(date):
    d = datetime.datetime.strptime(date,'%Y-%m-%d')
    return d.weekday()+1


def get_current_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # datatime类型转格式字符串
    monday = monday.strftime("%Y-%m-%d")
    sunday = sunday.strftime("%Y-%m-%d")
    return monday, sunday

def get_current_two_week():
    monday, sunday = datetime.date.today(), datetime.date.today()
    one_day = datetime.timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    monday-=one_day
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    sunday += one_day
    # datatime类型转格式字符串
    monday = monday.strftime("%Y-%m-%d")
    sunday = sunday.strftime("%Y-%m-%d")
    return monday, sunday

def get_current_mouth():
    first = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
    last = datetime.date(datetime.date.today().year, datetime.date.today().month + 1, 1) - datetime.timedelta(1)
    # datatime类型转格式字符串
    first = first.strftime("%Y-%m-%d")
    last = last.strftime("%Y-%m-%d")
    return first, last

def get_current_time_int():
    return time.time()


def isOnTheRoom(user_id):
    user = Users.query.filter(Users.user_id==user_id).first()
    updateTime = user.update_time
    if updateTime==None:
        updateTime=0
    if get_current_time_int() -  updateTime <= 90:
        return 'Y'
    else:
        return 'F'

def getUserTime(start_time,prograssTime,end_time=""):
    thisYear = datetime.datetime.now().year
    mouth = datetime.datetime.now().month
    if mouth>=9:
        mid_time = 2
    else:
        mid_time = 3
    if end_time!="":
        record = db.session.query(Users.user_id.label('user_id'),func.sum(Times.times_count).label('sum_count')).filter(Times.times_date>=start_time,Times.times_date<=end_time,Users.grade>=thisYear-mid_time,Users.type=='正式成员',Times.user_id==Users.user_id).group_by(Times.user_id).subquery()
    else:
        record = db.session.query(Users.user_id.label('user_id'),func.sum(Times.times_count).label('sum_count')).filter(Times.times_date>=start_time,Users.grade>=thisYear-mid_time,Users.type=='正式成员',Times.user_id==Users.user_id).group_by(Times.user_id).subquery()
    result = db.session.query(Users.user_id,Users.user_name,Users.sex,Users.avatar_path,record.c.sum_count).filter(Users.grade>=thisYear-mid_time,Users.type=='正式成员').outerjoin(record,record.c.user_id==Users.user_id).order_by(record.c.sum_count.desc()).all()
    person_list = []
    for index,re in enumerate(result):
        user_id,name,sex,head_path,time = re
        if time == None:
            time=0
        if int(time/3600)==0:
            count_time = str(int(time/60))+"分钟"
        else:
            count_time = str(int(time/3600))+"小时"+str(int((time%3600)/60))+"分钟"

        if head_path==None:
            if sex=='男':
                head_path=url_for('static',filename='image/默认头像-男.jpg')
            else:
                head_path=url_for('static',filename='image/默认头像-女.jpg')
        person_list.append({
            "num":index+1,
            "name":name,
            "time":count_time,
            "head":head_path,
            "isInTheRoom":isOnTheRoom(user_id),
            "prograss":int(min(max(10,int(100*(time/(prograssTime*60*60)))),100))
        })
    return person_list
if __name__ == '__main__':
    print(get_weekday('2019-09-08'))
