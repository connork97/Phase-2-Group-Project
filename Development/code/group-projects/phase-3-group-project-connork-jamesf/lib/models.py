#models.py

from sqlalchemy import ForeignKey, Column, DateTime, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer(), primary_key=True)
    productivity = Column(Integer())

    def __repr__(self):
        return f"Day(id={self.id}, " + \
            f"productivity={self.productivity})"
    
class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer(), primary_key=True)
    task = Column(String())
    hours = Column(Integer())
    minutes = Column(Integer())
    productivity = Column(Integer())

    def __repr__(self):
        return f"Activity(id={self.id}, " + \
            f"task={self.task}, " + \
            f"hours={self.hours}" + \
            f"minutes={self.minutes}" + \
            f"procutivity={self.productivity})"


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f"Friend(id={self.id}, " + \
            f"name={self.task})"
