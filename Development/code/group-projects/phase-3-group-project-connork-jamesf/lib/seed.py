from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from models import Day, Activity, Time, Friend

if __name__ == '__main__':

    print("Seeding 🌱...")
    print("Connecting to DB....")
    engine = create_engine('sqlite:///daily_schedule.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Session Created...")

    