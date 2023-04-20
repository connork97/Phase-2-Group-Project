#seed.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ipdb import set_trace


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
    session.query(Activity).delete()
    session.commit()


    # print("Creating day rows...")

    # monday = Day(name="Monday")
    # tuesday = Day(name="Tuesday")
    # wednesday = Day(name="Wednesday")
    # thursday = Day(name="Thursday")
    # friday = Day(name="Friday")
    # saturday = Day(name="Saturday")
    # sunday = Day(name="Sunday")

    # session.add_all([monday, tuesday, wednesday, thursday, friday, saturday, sunday])
    # session.commit()

   # print("All days of the week added!")
    

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


    snooze = Activity(task="Hit the snooze button...", hours=0, minutes=30, productivity=0)
    scroll_phone = Activity(task="Scroll on your phone for an hour.", hours=1, minutes=0, productivity=0)
    get_ready = Activity(task="Get out of bed and get ready for the day.", hours=0, minutes=30, productivity=1)

    breakfast = Activity(task="Eat breakfast.", hours=0, minutes=30, productivity=1)
    skip_breakfast = Activity(task="Skip breakfast and go to class.  You're running late!", hours=0, minutes=0, productivity=0)

    go_to_class = Activity(task="Go to class.", hours=0, minutes=0, productivity=3)
    chores = Activity(task="Do some chores around the house.", hours=0, minutes=45, productivity=2)
    study = Activity(task="Study for an hour.", hours=1, minutes=0, productivity=2)

    exercise = Activity(task="Go to the gym.", hours=1, minutes=30, productivity=2)
    hike = Activity(task="Go for a hike!", hours=2, minutes=0, productivity=1)
    touch_grass = Activity(task="Touch some grass.", hours=0, minutes=15, productivity=1)

    lunch = Activity(task="Grab some lunch.", hours=1, minutes=0, productivity=1)
    snack = Activity(task="Have a snack.", hours=0, minutes=15, productivity=0)

    video_games = Activity(task="Play your favorite video game.", hours=1, minutes=0, productivity=0)
    instrument = Activity(task="Play some music or start learning an instrument.", hours=0, minutes=30, productivity=2)

    watch_movie = Activity(task="Go to the movies with a friend.", hours=2, minutes=0, productivity=0)
    go_to_bar = Activity(task="Grab a drink with a friend.", hours=1, minutes=30, productivity=0)
    game_night = Activity(task="Host game night with a few friends!", hours=1, minutes=30, productivity=0)

    dinner = Activity(task="Eat dinner.", hours=1, minutes=0, productivity=1)

    watch_show = Activity(task="Watch your favorite show.", hours=1, minutes=0, productivity=0)
    read = Activity(task="Read a book.", hours=0, minutes=30, productivity=2)
    bedtime = Activity(task="Get ready for bed.", hours=1, minutes=0, productivity=1)
    sleep = Activity(task="Go to sleep!", hours=8, minutes=0, productivity=1)

    session.add_all([snooze, scroll_phone, get_ready, breakfast, skip_breakfast, go_to_class, chores, study, exercise, hike, touch_grass, lunch, snack, video_games, instrument, watch_movie, go_to_bar, game_night, dinner, watch_show, read, bedtime, sleep])
    session.commit()
    
    # current_time = time(current_time.hour + find_parentheses.hours, current_time.minute + find_parentheses.minutes).isoformat(timespec="minutes")
    # print("The new time is:", current_time)











    # set_trace()