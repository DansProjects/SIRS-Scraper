from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)

class Questions(Base):
    __tablename__ = "question"

class Answers(Base):
    __tablename__ = "answer"

