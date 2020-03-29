import sys

sys.path.append("..")
import datetime
from app import *
from Tools import Timer, Token, Function , GenerateCode
import json
from functools import wraps


def form_data(status=200, content=None):
    if content is None:
        content = {}
    data = {"code": status, "data": content}
    return json.dumps(data)


def autority(func):
    """
        登录装饰器
        若未登录则返回401错误，否则传入user属性
    :param func:
    :return:
    """
    @wraps(func)
    def comfirm(*args,**kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return form_data(401,"身份未被验证或登录信息过期")
        user = Token.verify_auth_token(token)
        if user:
            return func(user=user,*args,**kwargs)
        else:
            return form_data(401,"身份未被验证或登录信息过期")
    return comfirm


def abnormity(func):
    """
        异常捕获器
    :param func:
    :return:
    """
    @wraps(func)
    def ab(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception:
            return form_data(500,"服务器请求错误")
    return ab



@app.route('/api/web/getTime', methods=['GET'])
def getUserTime():
    """
        获取不同时间段的计时排行榜
        :param: type 0是一周 1是两周 2是本月 3是本学期 4是自定义
        :param: role 筛选的角色
        :param: start_time （自定义可选）开始时间
        :param: end_time （自定义可选）结束时间
        :param: start_grade （自定义可选）开始年级
        :param: end_grade （自定义可选）结束年级
        :return: 返回一个list，一行包括{num：序号，name：名字，time：计时的时间，avatar_path：头像地址，isInTheRoom：是否在工作室内，prograss：进度}
    """
    data = request.args
    type = data.get('type')
    role = data.get('role')
    start_time = data.get('start_time')
    start_grade = data.get('start_grade')
    end_grade = data.get('end_grade')
    end_time = data.get('end_time')
    if type is None:
        return form_data(200, "类型传输未传")
    if role is None:
        return form_data(200, "角色参数未传")
    type = int(type)
    if type == 0:
        start_time = Timer.getCurrentWeek()
    elif type == 1:
        start_time = Timer.getLastWeek()
    elif type == 2:
        start_time = Timer.getCurrentMouth()
    elif type == 3:
        start_time = Timer.getCurrentSemester()
    elif type == 4:
        if start_time is None or end_time is None:
            return form_data(200, "开始时间和结束时间参数未传")
        if start_grade is None or end_grade is None:
            return form_data(200, "开始年级和结束年级参数未传")
        data = Function.UserList(role, int(start_grade), end_grade).getTimeRank(start_time, end_time)
        return form_data(200,data)
    else:
        return form_data(200, "没有符合的类型")
    data = Function.UserList(role, Timer.getCurrentSchoolMemberSemester()).getTimeRank(start_time,str(datetime.datetime.today().date()))
    return form_data(200,data)


@app.route('/api/web/login', methods=['POST'])
@abnormity
def UserLogin():
    """
        用户登录回调函数
    :return: 返回用户的基本信息以及token信息
    """
    data = request.get_json()
    user_number = data.get('data').get('number')
    user_password = data.get('data').get('password')
    user = Users.query.filter(Users.account == user_number, Users.user_password == user_password).first()
    if user is None:
        return form_data(200,"用户不存在或密码错误")
    user_data = {
        "token": Token.generate_token(user.user_id),
        "user": user.getBaseInformation(),
        "work": Function.Server().isWork()
    }
    if user:
        return form_data(200, user_data)
    else:
        return form_data(200,"用户不存在或密码错误")


@app.route('/api/web/server', methods=['GET'])
def getServerStatus():
    """
        得到服务器状态回调函数
    :return: 返回当前服务器的状态
    """
    return form_data(200, {"server_status": Function.Server().isWork()})


@app.route('/api/web/user', methods=['GET'])
@autority
def getUser(user):
    """
        获得用户基本信息回调函数
    :param user: 要求登录
    :return:
    """
    return form_data(200, {"user": user.getBaseInformation()})


@app.route('/api/web/mac', methods=['GET'])
@autority
def getMac(user):
    """
        获得用户MAC地址的回调函数
    :param user: 要求登录
    :return:
    """
    return form_data(200, {"mac": user.getMacAddress()})


@app.route('/api/web/mac',methods=['POST'])
@autority
def setMac(user):
    """
        设置用户的Mac地址
    :param: user 要求登录
    :param: mobile_mac 手机Mac地址
    :param: computer_mac 电脑Mac地址
    :return:
    """
    data = request.get_json()
    mobile_mac = data.get('mobile_mac')
    computer_mac = data.get('computer_mac')
    user.setMac(mobile_mac,computer_mac)
    return form_data(200,"成功提交了修改MAC地址申请")



@app.route('/api/web/getMap', methods=['GET'])
@autority
def weekMap(user):
    """
        星期时间计时图回调函数
    :param user: 要求登录
    :return:
    """
    week_start = Timer.getCurrentWeek()
    t_data = DayTime.query.filter(DayTime.user_id == user.user_id,
                                  DayTime.time_date >= week_start,
                                  DayTime.time_point >= 8).all()
    week_map = [[0 for i in range(16)] for i in range(7)]
    for t in t_data:
        week_map[6 - int(t.time_date.weekday())][int(t.time_point) - 8] = t.time_count
    user_map = []
    for dy, day in enumerate(week_map):
        for hi, hours in enumerate(day):
            if hours == 0:
                continue
            user_map.append([dy, hi, hours])
    return form_data(200, {"map": user_map})


@app.route('/api/web/getGrade',methods=['GET'])
def getGrade():
    """
        生成可选大一大二的年级
    :return: 返回大一，大二的数组，比如【2017，2018】
    """
    return form_data(200,Timer.getCurrentGrade())


@app.route('/api/web/register',methods=['PUT'])
def register():
    """
        注册回调函数
        :param stdNumber 学号
        :param stdName 姓名
        :param password 密码
        :param code 验证码
        :param sex 性别
        :param grade 年级 输入0或者1
    :return:
    """
    data = request.get_json()
    stdNumber = data.get('stdNumber')
    stdName = data.get('stdName')
    password = data.get('password')
    code = data.get('code')
    sex = data.get('sex')
    grade = data.get('grade')
    if stdNumber is None or stdName is None or password is None or code is None or sex is None or grade is None:
        return form_data(200,"请填写相关的参数")
    grade = Timer.getCurrentGrade()[int(grade)]
    if Users.query.filter(Users.account==stdNumber).first() is not None:
        return form_data(200,"学号已经存在")
    if Users.query.filter(Users.user_name==stdName).first() is not None:
        return form_data(200,"姓名已经存在")
    if not GenerateCode.VerifyCode(code):
        return form_data(200,"验证码错误")
    user = Users(account=stdNumber,user_name=stdName,user_password=password,sex=sex,grade=grade,type='待审核')
    db.session.add(user)
    db.session.commit()
    return form_data(200,"注册成功")


@app.route('/api/web/getCode',methods=['GET'])
def getCode():
    """
        获得注册码
    :return:
    """
    return form_data(200,GenerateCode.GenerateCode())

@app.route('/api/web/setAvatar',methods=['POST'])
@autority
def setAvatar(user):
    image = request.files.get('file')
    image_src = user.setAvatar(image)
    return form_data(200,image_src)