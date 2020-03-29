from exts import db
from sqlalchemy import func
import time
from flask import url_for
import random
from Tools import Timer
import hashlib
import re
import os


class Users(db.Model):
    """
        用户表
        记录用户基本信息的表
        @:param account 学号
        @:param user_name 姓名
        @:param user_password 用户密码
        @:param sex 性别
        @:param grade 年级
        @:param type 用户类型，比如用正式成员，普通成员，退休成员，考核成员,测试人员等
        @:param update_time 更新时间，用于判断是否在工作室内，若查询当前时间-更新时间大于90s则代表不在工作室
        @:param avatar_path 头像地址
    """
    __tablename__ = 'timer_users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.VARCHAR(11), nullable=True, unique=True)
    user_name = db.Column(db.VARCHAR(20), nullable=True, unique=True)
    user_password = db.Column(db.VARCHAR(32), nullable=True)
    sex = db.Column(db.VARCHAR(6), nullable=True)
    grade = db.Column(db.VARCHAR(4), nullable=True)
    type = db.Column(db.VARCHAR(10))
    update_time = db.Column(db.Integer)
    avatar_path = db.Column(db.VARCHAR(200))

    def getBaseInformation(self):
        """
            获取该用户的基本信息
            @:return 当前用户头像地址、id、用户名、性别、是否在工作室、现有时间的列表
        """
        time = db.session.query(func.sum(Times.times_count)).filter(Times.times_date >= Timer.getCurrentWeek(),
                                                                    Times.user_id == self.user_id).group_by(
            Times.user_id).first()
        if time is None:
            time = 0
        else:
            time = time[0] / 60
        second = str(100 + int(random.randint(1, 59)))[1:]
        if self.avatar_path is None:
            if self.sex == '男':
                head_path = url_for('static', filename='image/man.jpg')
            else:
                head_path = url_for('static', filename='image/women.jpg')
        else:
            head_path = self.avatar_path
        information = {
            "head": head_path,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "sex": self.sex,
            "inRoom": self.isOnTheRoom(),
            "time": {
                "hours": str(100 + int(time / 60))[1:],
                "mintus": str(100 + int(time % 60))[1:],
                "seconds": str(second),
            },"type":self.type
        }
        return information

    def isOnTheRoom(self):
        """
            判断该用户是否在工作室中
            @:return 是否在工作室真假值
        """
        updateTime = self.update_time
        if updateTime == None:
            updateTime = 0
        if int(time.time()) - updateTime <= 90:
            return True
        else:
            return False

    def getMacAddress(self):
        """
            获取该用户MAC地址
            @:return 返回手机和电脑的MAC地址
        """
        user_mobile_mac = Mac.query.filter(Mac.user_id == self.user_id, Mac.type == 1).first()
        user_computer_mac = Mac.query.filter(Mac.user_id == self.user_id, Mac.type == 2).first()
        mobile_mac = ''
        computer_mac = ''
        if user_mobile_mac != None:
            mobile_mac = user_mobile_mac.mac
        if user_computer_mac != None:
            computer_mac = user_computer_mac.mac
        return {"mobile": mobile_mac, "computer": computer_mac}

    # TODO 查询用户当前在线时间
    def getOnlineTime(self):
        pass

    # TODO 查询该天该用户的计时图
    def getDayTime(self, time_date):
        pass

    # TODO 查询头像地址
    def getAvatarPath(self,file):
        pass

    # TODO 增加头像
    def setAvatar(self,file):
        basepath = os.path.dirname(__file__)
        pic_name = file.filename+str(time.time())+self.user_name
        md5 = hashlib.md5()
        md5.update(str(pic_name).encode('utf-8'))
        pic_name = md5.hexdigest()+'.jpg'
        file.save('static/avatar/'+pic_name)
        print(basepath+'static/avatar/'+pic_name)
        if self.avatar_path != None and os.path.exists(self.avatar_path):
            os.remove(self.avatar_path)
        self.avatar_path = url_for('static',filename='avatar/'+pic_name)
        db.session.commit()
        return self.avatar_path

    def setMac(self, mobile_mac, computer_mac):
        """
            设置Mac地址，若不存在Mac地址曾新增
        :param mobile_mac: 手机的Mac地址
        :param computer_mac: 电脑的Mac地址
        :return:
        """
        def upMac(mac):
            if mac is None:
                mac = ""
            return str(mac).upper().replace(":", "-")
        def isLegal(mac):
            ac = re.search("(..)-(..)-(..)-(..)-(..)-(..)", mac)
            if ac is None:
                return False
            else:
                return True
        mob = upMac(mobile_mac)
        com = upMac(computer_mac)
        mobile_mac = Mac.query.filter(Mac.user_id==self.user_id,Mac.type==1).first()
        computer_mac = Mac.query.filter(Mac.user_id==self.user_id,Mac.type==2).first()
        if mobile_mac is None and isLegal(mob):
            mobile_mac = Mac(mac=mob,user_id=self.user_id,type='1')
            db.session.add(mobile_mac)
        elif mobile_mac and isLegal(mob):
            mobile_mac.mac = mob
        if computer_mac is None and isLegal(com):
            computer_mac = Mac(mac=com,user_id=self.user_id,type='2')
            db.session.add(computer_mac)
        elif computer_mac and isLegal(com):
            computer_mac.mac = com
        db.session.commit()

    # TODO 更新时间
    def updateTime(self):
        pass


class Times(db.Model):
    """
        计时表
        用于在统计用户在这一天中一共记录了多少秒
        @:param user_id 外接User表的id
        @:param times_date 记录用户是在那一天 使用date类型
        @:param times_count 记录用户这一天的秒数 使用Integer类型
    """
    __tablename__ = 'timer_times'
    times_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('timer_users.user_id'), nullable=True)
    times_date = db.Column(db.Date, nullable=True)
    times_count = db.Column(db.Integer, nullable=True)


class Notice(db.Model):
    """
        公告表
        用于公告一些话
        @:param notice_date 指定的公告时间
        @:param notice_content 公告的内容
        @:param notice_createTime 公告的产生时间
    """
    __tablename__ = 'timer_notice'
    notice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notice_date = db.Column(db.VARCHAR(10), nullable=True)
    notice_content = db.Column(db.VARCHAR(300), nullable=True)
    notice_createTime = db.Column(db.DateTime, nullable=True)


class Mac(db.Model):
    """
        MAC地址表
        用于记录用户的MAC地址，用于路由器爬虫的识别人员
        @:param user_id 用户的ID号
        @:param mac MAC地址
        @:param type MAC的类型，现在1是手机类型，2是电脑类型
    """
    __tablename__ = 'record_mac'
    mac_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('timer_users.user_id'))
    mac = db.Column(db.VARCHAR(20), nullable=True, unique=True)
    type = db.Column(db.VARCHAR(10), nullable=True)


class DayTime(db.Model):
    """
        一天24小时时间表
        用于绘制24小时到寝图，记录每个小时过来的分钟数
        @:param user_id 用户的ID号
        @:param time_date 该天的日期
        @:param time_point 该天的时间点
        @:param time_count 该天该时间点的在线分钟数
    """
    __tablename__ = 'record_daytime'
    daytime_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('timer_users.user_id'))
    time_date = db.Column(db.Date)
    time_point = db.Column(db.VARCHAR(4), nullable=True)
    time_count = db.Column(db.VARCHAR(2), nullable=True)
