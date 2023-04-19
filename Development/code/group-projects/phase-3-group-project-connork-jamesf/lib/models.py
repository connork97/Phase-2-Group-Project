from sqlalchemy import ForeignKey, Column, DateTime, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer(), primary_key=True)
    day = Column(String())

    def __repr__(self):
        return f"Day(id={self.id}, " + \
            f"name={self.day})"
    
class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer(), primary_key=True)
    task = Column(String())
    time_id = Column(Integer(), ForeignKey("time.id"))
    friend_id = Column(Integer(), ForeignKey("friend.id"))

    def __repr__(self):
        return f"Activity(id={self.id}, " + \
            f"task={self.task}, " + \
            f"time_id={self.time_id}, " + \
            f"friend_id={self.friend_id if self.friend_id else None})"

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer(), primary_key=True)
    time = Column(String())

    def __repr__(self):
        return f"Time(id={self.id}, " + \
            f"time={self.task})"

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f"Friend(id={self.id}, " + \
            f"name={self.task})"
