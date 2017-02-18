from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
import configparser
from sqlalchemy import Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import json

Base = declarative_base()

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    course_name = Column(String(250))
    year = Column(Integer)
    semester = Column(String(25))
    school = Column(Integer)
    department = Column(Integer)
    course = Column(Integer)
    section = Column(Integer)
    instructor = Column(String(250))
    source = Column(String(250))
    enrollments = Column(Integer())
    responses = Column(Integer())
    created_at = Column(String(250))
    updated_at = Column(String(250))

class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    question_text = Column(BLOB)
    question_type = Column(String(250))
    created_at = Column(String(250))
    updated_at = Column(String(250))

class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    rating_1 = Column(Integer)
    rating_2 = Column(Integer)
    rating_3 = Column(Integer)
    rating_4 = Column(Integer)
    rating_5 = Column(Integer)
    blank = Column(Integer)
    created_at = Column(String(250))
    updated_at = Column(String(250))

class Database():

    def connect(self):
        cp = configparser.RawConfigParser()
        configFilePath = 'config.txt'
        cp.read(configFilePath)

        mysql_host = cp.get("mysql-config", "mysql_host")
        mysql_user = cp.get("mysql-config", "mysql_user")
        mysql_password = cp.get("mysql-config", "mysql_password")
        mysql_database = cp.get("mysql-config", "mysql_database")

        connection_string = "mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"\
            .format(db_user=mysql_user, db_password=mysql_password, db_host=mysql_host, db_name=mysql_database)

        return connection_string

db_connect = Database()
connection_string = db_connect.connect()

engine = create_engine(connection_string)

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
