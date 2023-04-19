#seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Base

if __name__ == '__main__':

    print("Seeding 🌱...")
    print("Connecting to DB....")
    engine = create_engine('sqlite:///daily_schedule.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(session, "Session Created...")

    print("Creating day rows...")

    # monday = Day(name="Monday")
    # tuesday = Day(name="Tuesday")
    # wednesday = Day(name="Wednesday")
    # thursday = Day(name="Thursday")
    # friday = Day(name="Friday")
    # saturday = Day(name="Saturday")
    # sunday = Day(name="Sunday")

    # session.add(monday)
    # # session.add_all([monday, tuesday, wednesday, thursday, friday, saturday, sunday])
    # session.commit()

    print("All days of the week added!")
    