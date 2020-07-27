from datetime import datetime
from .sql import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import app


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)
    birthday = db.Column(db.Date)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum('student', 'teacher','administrator'), nullable=False)
    permission = db.Column(db.Integer, nullable=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


class UserList(db.Model):
    __tablename__ = 'user_list'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)
    role = db.Column(db.Enum('student', 'teacher','administrator'), nullable=False)


class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'))
    title = db.Column(db.Unicode(50), nullable=False)
    content = db.Column(db.UnicodeText)
    pic = db.Column(db.String(150))
    time_start = db.Column(db.DateTime, default=datetime.now)
    time_end = db.Column(db.DateTime, nullable=False)
    anonymous = db.Column(db.Boolean, nullable=False)
    multiple = db.Column(db.Boolean, nullable=False)
    academy = db.Column(db.JSON)
    grade = db.Column(db.JSON)
    person = db.Column(db.JSON)
    user = db.relationship("User", backref="vote")


class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.BigInteger, primary_key=True)
    group = db.Column(db.Unicode(20), nullable=False)
    content = db.Column(db.Unicode(50), nullable=False)
    vote_id = db.Column(db.BigInteger, db.ForeignKey(
        'vote.id'), nullable=False)
    count = db.Column(db.BigInteger, nullable=False)
    vote = db.relationship("Vote", backref="option")


class VoteHistory(db.Model):
    __tablename__ = 'vote_history'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey(
        'user.id'), nullable=False)
    vote_id = db.Column(db.BigInteger, db.ForeignKey(
        'vote.id'), nullable=False)
    option_id = db.Column(db.BigInteger, db.ForeignKey(
        'option.id'), nullable=False)
    user = db.relationship("User", backref="vote_history")
    vote = db.relationship("Vote", backref="vote_history")
    option = db.relationship("Option", backref="vote_history")


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'))
    title = db.Column(db.Unicode(50), nullable=False)
    content = db.Column(db.UnicodeText)
    user = db.relationship("User", backref="feedback")
