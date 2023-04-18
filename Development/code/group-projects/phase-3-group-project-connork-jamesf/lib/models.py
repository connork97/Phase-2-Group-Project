from sqlalchemy import ForeignKey, Column, DateTime, Integer, String

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base

# class Day(Base):
#     __tablename__ = "days"

#     id = Column(Integer(), primary_key=True)
#     day = Column(String())
#     schedule_id = Column(Integer(), ForeignKey("schedule.id"))  #  Does schedule belong to day or day belong to schedule?  Probably schedule to day I think.

#     def __repr__(self):
#         return f"Day(id={self.id}, " + \
#             f"name={self.day}" + \
#             f"schedule_id={self.schedule_id})"
    
# class Schedule(Base):
#     __tablename__ = "schedules"

#     id = Column(Integer(), primary_key=True)
#     time_ids = Column(String()) # ==> Is this going to be a list of times?  Since the times will vary from day to day?
#     activity_ids = Column(String()) # ==> How do we want to allow for as many activities as we want?  Similar problem to "time" where there will be more than one and they change by day.
#     friend_ids = Column(Integer)
#     day_id = Column(Integer(), ForeignKey("day.id")) # ==>  Does day belong to schedule or schedule belong to day?  Probably schedule to day.


# class Activity(Base):
#     __tablename__ = "activities"
    
#     id = Column(Integer(), primary_key=True)
#     activity1 = Column(String())
#     activity2 = Column(String())
#     activity3 = Column(String())
#     activity4 = Column(String())
#     activity5 = Column(String())
#     activity6 = Column(String())
#     activity7 = Column(String())
#     activity8 = Column(String())
#     activity9 = Column(String())
#     activity10 = Column(String())

# class Friend(Base):
#     __tablename__ = "friends"

#     id = Column(Integer(), primary_key=True)
#     connor = Column(String())
#     james = Column(String())
#     bill = Column(String())
#     wally = Column(String())
#     shelby = Column(String())
#     cole = Column(String())
#     oli = Column(String())
#     holden = Column(String())
