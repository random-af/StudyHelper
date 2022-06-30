from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


'''class QuestionStats(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct_cnt = db.Column(db.Integer)
    wrong_cnt = db.Column(db.Integer)

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'question_id'),)'''


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    acc_name = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    themes = db.relationship('Theme')


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150), unique=True)
    questions = db.relationship('Question')

    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='_user_theme_uc'),)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'))
    question = db.Column(db.String(5000))
    answer = db.Column(db.String(5000))
    comment = db.Column(db.String(10000))
    correct_cnt = db.Column(db.Integer, default=0)
    incorrect_cnt = db.Column(db.Integer, default=0)
