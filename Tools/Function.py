import time
import sys
import datetime
import re

sys.path.append("..")
from models import *


class UserList:
    """
        用户组操作
        :param role 角色
        :param search_start_grade = 搜索开始的年级
        :param search_end_grade = 搜索结束的年级
    """
    role = ""
    search_start_grade = ""
    search_end_grade = ""

    def __init__(self, role, start_grade, end_grade=datetime.datetime.now().year):
        self.role = role
        self.search_start_grade = start_grade
        self.search_end_grade = end_grade

    def getUserIdList(self):
        """
            获取用户ID列表
            :return: 所有用户的ID列表以及姓名，{id:,name:}
        """
        data = []
        users = Users.query.filter(Users.type == self.role, Users.grade >= self.search_start_grade,
                                   Users.grade <= self.search_end_grade).all()
        for user in users:
            data.append({"id": user.user_id, "name": user.user_name})
        return data

    def getTimeRank(self, start_time, end_time):
        """
            根据时间获取当前计时器的排行榜
            :param start_time:
            :param end_time:
            :return:计时排行，从上到下，一行有序号，id，名字，时间（小时，分钟，时间戳，间隔星期），进度条长度，头像地址，性别，是否在工作室
        """
        record = db.session.query(Users.user_id.label('user_id'),
                                  func.sum(Times.times_count).label('sum_count')).filter(Times.times_date >= start_time,
                                                                                         Times.times_date <= end_time,
                                                                                         Users.grade >= self.search_start_grade,
                                                                                         Users.grade <= self.search_end_grade,
                                                                                         Users.type == self.role,
                                                                                         Times.user_id == Users.user_id).group_by(
            Times.user_id).subquery()
        result = db.session.query(Users,
                                  record.c.sum_count).filter(
                Users.grade >= self.search_start_grade,Users.grade <= self.search_end_grade, Users.type == self.role).outerjoin(record,
                                                                                    record.c.user_id == Users.user_id).order_by(
                record.c.sum_count.desc()).all()
        person_list = []
        for index, re in enumerate(result):
            user, time = re
            user_id = user.user_id
            name = user.user_name
            if user.avatar_path is None:
                if user.sex == '男':
                    head_path = url_for('static', filename='image/man.jpg')
                else:
                    head_path = url_for('static', filename='image/women.jpg')
            else:
                head_path = user.avatar_path
            sex = user.sex
            if time == None:
                time = 0
            prograss = int(min(max(10, int(100 * (time / (Timer.getTwoTimeHaveWeek(start_time,end_time) * 24 * 60 * 60)))), 100))
            hours = int(time/3600)
            minutes = int((time % 3600) / 60)
            person_list.append({
                "num": index + 1,
                "id":user_id,
                "name": name,
                "grade": user.grade,
                "time": {
                    "hours":hours,
                    "minutes":minutes,
                    "int":int(time),
                    "week":int(Timer.getTwoTimeHaveWeek(start_time,end_time))
                },
                "prograss": prograss,
                "avatar_path":head_path,
                "sex":sex,
                "isInTheRoom":user.isOnTheRoom()
            })
        return person_list


class Server:
    """
        服务器类，使用的账号是id为5的测试账号
    """
    server = ""

    def __init__(self):
        self.server = Users.query.filter(Users.user_id==5).first()

    def isWork(self):
        return self.server.isOnTheRoom()

