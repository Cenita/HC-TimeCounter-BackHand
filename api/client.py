import sys

sys.path.append("..")
from app import *
from Tools import Timer, Token, Function , GenerateCode
import datetime
import json
from functools import wraps


@app.route('/addTime',methods=['POST'])
def addTime():
    data = request.get_json()
    mac_list = data.get('macList')
    #更新检查时间
    admin = Users.query.filter(Users.user_id==5).first()
    admin.update_time=time.time()
    add_user = []
    add_user_name = []
    back_data = {
        'status': 'ok',
    }
    if mac_list!=None:
        for mac in mac_list:
            try:
                #遍历一边发送过来的mac地址
                user_mac = Mac.query.filter(Mac.mac==mac).first()
                if user_mac==None:
                    continue
                add_user.append(user_mac.user_id)
            except Exception:
                pass
    add_user = list(set((add_user)))
    for user_id in add_user:
        try:
            user = Users.query.filter(Users.user_id == user_id).first()
            add_user_name.append(user.user_name)
            user.update_time=time.time()
            daytime = DayTime.query.filter(DayTime.user_id==user.user_id,DayTime.time_point==datetime.datetime.now().hour,DayTime.time_date==datetime.date.today()).first()
            allTime = Times.query.filter(Times.user_id==user.user_id,Times.times_date==datetime.date.today()).first()
            #增加小时数据
            if daytime:
                daytime.time_count=int(daytime.time_count)+1
            else:
                db.session.add(DayTime(user_id=user.user_id,time_point=datetime.datetime.now().hour,time_count=1,time_date=datetime.date.today()))
            #增加这一天的数据
            if allTime:
                allTime.times_count=int(allTime.times_count)+60
            else:
                db.session.add(Times(user_id=user.user_id,times_date=datetime.date.today(),times_count=60))
        except Exception:
            pass
    db.session.commit()
    back_data['addUser']=add_user_name
    return json.dumps(back_data)


@app.route('/addUserTime',methods=['POST'])
def addUserTime():
    js = request.get_json()
    user_list = js.get('user_list')
    success_name = []
    for user in user_list:
        try:
            user_name = user.get('user_name')
            add_time = user.get('add_time')
            addUserTimeByUserName(user_name,add_time)
            success_name.append(user_name)
        except Exception:
            pass
    return json.dumps({"status":'ok',"success_user":success_name})


def addUserTimeByUserName(user_name,time):
    user = Users.query.filter(Users.user_name == user_name).first()
    time_date = Times.query.filter(Times.user_id == user.user_id, Times.times_date == datetime.date.today()).first()
    if time_date == None:
        db.session.add(Times(user_id=user.user_id,times_date=datetime.date.today(),times_count=60*time))
    else:
        time_date.times_count = time_date.times_count+time*60
    db.session.commit()