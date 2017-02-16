from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

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
    source = Column(String(250))
    enrollments = Column(Integer())
    responses = Column(Integer())
    created_at = Column(String(250))
    updated_at = Column(String(250))

class Questions(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    question_text = Column(BLOB)
    question_type = Column(String(250))
    created_at = Column(String(250))
    updated_at = Column(String(250))

class Answers(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    question_id = Column(Integer)
    rating_1 = Column(Integer)
    rating_2 = Column(Integer)
    rating_3 = Column(Integer)
    rating_4 = Column(Integer)
    rating_5 = Column(Integer)
    blank = Column(Integer)
    created_at = Column(String(250))
    updated_at = Column(String(250))

#engine = create_engine('sqlite:///sirs.db')
engine = create_engine('mysql+pymysql://root:@localhost/test')

Base.metadata.create_all(engine)