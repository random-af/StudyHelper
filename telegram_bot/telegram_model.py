import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, mapped_column


Base = declarative_base()


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    id = mapped_column(Integer, primary_key=True)
    current_bundle_id = mapped_column(Integer, nullable=True)
    bundles = relationship('Bundle', back_populates="user")


class Bundle(Base):
    __tablename__ = 'bundle'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('telegram_user.id'))
    name = Column(String(50))
    user = relationship('TelegramUser', back_populates='bundles')
    questions = relationship('Question', back_populates='bundle')


class Message(Base):
    __tablename__ = 'message'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)  # utochnit'
    sender_id = mapped_column(ForeignKey('telegram_user.id'))
    type = None
    date = None


class Question(Base):
    __tablename__ = 'question'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    question = Column(String(150))
    answer = Column(String(150))
    bundle_id = mapped_column(ForeignKey('bundle.id'))
    bundle = relationship('Bundle', back_populates='questions')
    #tags


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    bundle_id = Column(Integer)
    #questions


engine = create_engine("sqlite:///C:\\Users\\norxo\\PycharmProjects\\Study_helper\\database\\telegram_bot.db", echo=True)
Base.metadata.create_all(bind=engine)
