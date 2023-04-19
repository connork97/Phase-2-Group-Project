#seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ipdb import set_trace

from datetime import time, timedelta, datetime

from models import (Base, Day, Friend, Activity)

if __name__ == '__main__':

    print("Seeding 🌱...")
    print("Connecting to DB....")
    engine = create_engine('sqlite:///daily_routine.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(session, "Session Created...")

    print("Dropping Tables...")
    session.query(Day).delete()
    session.query(Friend).delete()
    # session.query(Activity).delete()
    session.commit()


    print("Creating day rows...")

    monday = Day(name="Monday")
    tuesday = Day(name="Tuesday")
    wednesday = Day(name="Wednesday")
    thursday = Day(name="Thursday")
    friday = Day(name="Friday")
    saturday = Day(name="Saturday")
    sunday = Day(name="Sunday")

    session.add_all([monday, tuesday, wednesday, thursday, friday, saturday, sunday])
    session.commit()

    print("All days of the week added!")
    

    connor = Friend(name="Connor")
    james = Friend(name="James")
    cole = Friend(name="Cole")
    bill = Friend(name="Bill")
    shelby = Friend(name="Shelby")
    holden = Friend(name="Holden")
    oli = Friend(name="Oli")
    wally = Friend(name="Wally")

    session.add_all([connor, james, cole, bill, shelby, holden, oli, wally])
    session.commit()
    
    print("All friends added!")
    # time.isoformat(timespec="minutes")
    current_time = time(hour=8, minute=0)
    print("The current time is:", current_time.isoformat(timespec="minutes"))
    # current_time = time(hour=current_time.hour + 1, minute=current_time.minute).isoformat(timespec="minutes")
    # print("The new time is:", current_time)

    find_parentheses = Activity(task="wasting time", hours=2, minutes=30, friend_id=1)
    session.add(find_parentheses)
    session.commit()
    
    # current_time = time(current_time.hour + find_parentheses.hours, current_time.minute + find_parentheses.minutes).isoformat(timespec="minutes")
    # print("The new time is:", current_time)
    set_trace()