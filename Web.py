from app import *
import Timer
import datetime
import TPLINKGETMAC
import json
import random
import re
@app.route('/')
def index():
    data = {}
    if 'user_id' in session:
        user_mac = Mac.query.filter(Mac.user_id==session['user_id']).first()
        if user_mac == None:
            return redirect(url_for('setting'))
        user = Users.query.filter(Users.user_id==session['user_id']).first()
        time = db.session.query(func.sum(Times.times_count)).filter(Times.times_date>=Timer.get_current_week()[0],Times.user_id==user.user_id).group_by(Times.user_id).first()
        if time==None:
            time=0
        else:
            time=time[0]/60
        second = str(100+int(random.randint(1,59)))[1:]
        if Timer.isOnTheRoom(user.user_id)=='F':
            second="00"
        user_list = {
            'inTheRoom':Timer.isOnTheRoom(user.user_id),
            'user_name':user.user_name,
            'Hours':str(100+int(time/60))[1:],
            'Minutes':str(100+int(time%60))[1:],
            'Seconds':second
        }
        data['user']=user_list
    data['_work']=Timer.isOnTheRoom(5)
    data["one_week"] = Timer.getUserTime(start_time=Timer.get_current_week()[0],prograssTime=24)
    data["one_two_week"] = Timer.getUserTime(start_time=Timer.get_current_two_week()[0],prograssTime=24*2)
    data["one_mouth"] = Timer.getUserTime(start_time=Timer.get_current_mouth()[0],prograssTime=24*4)
    data["one_semester"] = Timer.getUserTime(start_time=Timer.get_current_semester(),prograssTime=24*14)
    return render_template('index.html',**data)

@app.route('/login',methods=['GET','POST'])
def login():
    session.clear()
    if request.method=='GET':
        return render_template('login.html')
    else:
        user_number = request.form.get('stdNumber')
        password = request.form.get('stdPassword')
        user = Users.query.filter(Users.account==user_number,Users.user_password==password).first()
        data = {
            "status":200,
            "content":''
        }
        if user:
            session['user_id']=user.user_id
            session['user_name']=user.user_name
            if user.avatar_path == None:
                if user.sex == '男':
                    session['avatar'] = url_for('static', filename='image/默认头像-男.jpg')
                else:
                    session['avatar'] = url_for('static', filename='image/默认头像-女.jpg')
            else:
                session['avatar'] = user.avatar_path
            data['content']='登录成功'
            return json.dumps(data)
        else:
            data['status']='400'
            data['content']='密码错误'
            return json.dumps(data)

@app.route('/HoursCome',methods=['POST'])
def HoursCome():
    if 'user_id' in session:
        week_start,week_end = Timer.get_current_week()
        print(week_start,week_end)
        t_data = DayTime.query.filter(DayTime.user_id == session['user_id'],
                                 DayTime.time_date >=week_start,DayTime.time_date<=week_end,DayTime.time_point>=8).all()
        week_map = [[0 for i in range(16)] for i in range(7)]
        for t in t_data:
            week_map[6-int(t.time_date.weekday())][int(t.time_point)-8]=t.time_count
        user_map=[]
        for dy,day in enumerate(week_map):
            for hi,hours in enumerate(day):
                if hours == 0:
                    continue
                user_map.append([dy,hi,hours])
        return json.dumps({'week_map':user_map})
    else:
        return '666'

@app.route('/loginout')
def loginOut():
    session.clear()
    return redirect(url_for('index'))

@app.route('/setting',methods=['GET','POST'])
def setting():
    if request.method=='GET':
        if 'user_id' in session:
            user_mobile_mac = Mac.query.filter(Mac.user_id==session['user_id'],Mac.type==1).first()
            user_computer_mac = Mac.query.filter(Mac.user_id==session['user_id'],Mac.type==2).first()
            mobile_mac = ''
            computer_mac = ''
            if user_mobile_mac != None:
                mobile_mac = user_mobile_mac.mac
            if user_computer_mac != None:
                computer_mac = user_computer_mac.mac
            return render_template('setting.html',mobile_mac=mobile_mac,computer_mac=computer_mac)
        else:
            return redirect(url_for('login'))
    else:
        mobile_mac = request.form.get('mobile_mac')
        computer_mac = request.form.get('computer_mac')
        mbmac = addMac(mobile_mac,1)
        cpmac = addMac(computer_mac,2)
        data = {
            "status":max(mbmac.get('status'),cpmac.get('status')),
            "mobile":mbmac,
            "computer":cpmac
        }
        return json.dumps(data)


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



def addMac(mac,type):
    mac = str(mac).upper()
    if mac=="":
        return {"status":200}
    mac_gourp = re.findall('(..)-(..)-(..)-(..)-(..)-(..)', mac)
    data = {
        "status": 400,
        "content": "error"
    }
    if mac_gourp == []:
        mac_gourp = re.findall('(..):(..):(..):(..):(..):(..)', mac)
        if mac_gourp == []:
            data['content'] = '格式不符合要求，请确保是类似于( XX:XX:XX:XX:XX:XX )格式的字符串'
            return data
    mac = "-".join(mac_gourp[0])
    #检查这个地址是否已经存在
    #若存在则检查当前属性是否属于该用户
    #以及是否属于该用户的设备类型
    check_mac = Mac.query.filter(Mac.mac==mac).first()
    if check_mac != None and (session['user_id']!=check_mac.user_id or (session['user_id']==check_mac.user_id and str(type)!=str(check_mac.type))):
        data['content'] = '该MAC地址已经存在'
        return data


    if 'user_id' in session:
        user_mac = Mac.query.filter(Mac.user_id == session['user_id'],Mac.type==type).first()
        if user_mac == None:
            user_mac = Mac(user_id=session['user_id'], mac=mac,type=type)
            db.session.add(user_mac)
            db.session.commit()
        else:
            user_mac.mac = mac
            db.session.commit()
        data['status'] = 200
        data['content'] = '保存成功'
        return data
    else:
        return data

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