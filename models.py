from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'rank'
    user_id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(255), nullable=False)
    user_dc = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    xp_accumulated = db.Column(db.Integer, nullable=False)
    lvl = db.Column(db.Integer, nullable=False)
    #timer = db.Column(db.DateTime, nullable=False)
    server_id = db.Column(db.Integer, nullable=False)

    def __init__(self, avatar_url, username, points_1, points_2, status):
        self.avatar_url = avatar_url
        self.username = username
        self.points_1 = points_1
        self.points_2 = points_2
        self.status = status

class Log(db.Model):
    __tablename__ = 'user_activity_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    multiplier = db.Column(db.Numeric(5,2), nullable=False)
    xp_multiplied = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    channel = db.Column(db.String(100), nullable=False)

    def __init__(self, datetime, user, type, xp, multiplier, xp_multiplier, level, channel):
        self.datetime = datetime
        self.user = user
        self.type = type
        self.xp = xp
        self.multiplier = multiplier
        self.xp_multiplier = xp_multiplier
        self.level = level
        self.channel = channel