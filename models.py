from exts import db
class Users(db.Model):
    __tablename__ = 'timer_users'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    account = db.Column(db.VARCHAR(11),nullable=True,unique=True)
    user_name = db.Column(db.VARCHAR(20),nullable=True,unique=True)
    user_password = db.Column(db.VARCHAR(32),nullable=True)
    sex = db.Column(db.VARCHAR(6),nullable=True)
    grade = db.Column(db.VARCHAR(4),nullable=True)
    type = db.Column(db.VARCHAR(10))
    update_time = db.Column(db.Integer)
    avatar_path = db.Column(db.VARCHAR(50))

class Times(db.Model):
    __tablename__ = 'timer_times'
    times_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('timer_users.user_id'),nullable=True)
    times_date = db.Column(db.Date,nullable=True)
    times_count = db.Column(db.Integer,nullable=True)

class Apply(db.Model):
    __tablename__ = 'timer_apply'
    apply_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('timer_users.user_id'))
    apply_start_time = db.Column(db.DateTime,nullable=True)
    apply_end_time = db.Column(db.DateTime)
    apply_info = db.Column(db.VARCHAR(50),nullable=True)
    apply_status = db.Column(db.Integer,nullable=True)

class Notice(db.Model):
    __tablename__ = 'timer_notice'
    notice_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    notice_date = db.Column(db.VARCHAR(10),nullable=True)
    notice_content = db.Column(db.VARCHAR(300),nullable=True)
    notice_createTime = db.Column(db.DateTime,nullable=True)

class Mac(db.Model):
    __tablename__ = 'record_mac'
    mac_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('timer_users.user_id'))
    mac = db.Column(db.VARCHAR(20),nullable=True,unique=True)
    type = db.Column(db.VARCHAR(10),nullable=True)

class DayTime(db.Model):
    __tablename__ = 'record_daytime'
    daytime_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('timer_users.user_id'))
    time_date = db.Column(db.Date)
    time_point = db.Column(db.VARCHAR(4),nullable=True)
    time_count = db.Column(db.VARCHAR(2),nullable=True)