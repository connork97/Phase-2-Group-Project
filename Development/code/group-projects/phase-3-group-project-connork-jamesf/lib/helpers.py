from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (Base, Friend, Activity, Day)

from ipdb import set_trace

engine = create_engine('sqlite:///daily_routine.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Time:
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes

    def __str__(self):
        return '{:02d}:{:02d}'.format(self.hours, self.minutes)

    def add_minutes(self, minutes):
        self.minutes += minutes
        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes %= 60
        if self.hours > 12:
            self.hours -= 12

    def add_hours(self, hours):
        self.hours += hours
        if self.hours > 12:
            self.hours -= 12

current_time = Time(6, 30)

all_activities = session.query(Activity).all()
all_friends = session.query(Friend).all()
# all_days = session.query(Day).all()

for activity in all_activities:
    print(activity.task, activity.hours, activity.minutes, activity.id)

# days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# days_index = 0

productivity_score = 0

def general_update(chosen_act):
    global productivity_score
    current_time.add_hours(chosen_act.hours)
    current_time.add_minutes(chosen_act.minutes)
    productivity_score += chosen_act.productivity

def good_morning():
    global productivity_score
    productivity_score = 0
    i = 0
    j = 1
    while i in range(0, 3):
        print(f"{j}: {all_activities[i].task}")
        i += 1
        j += 1
    first_input = input()
    chosen_act = all_activities[int(first_input) - 1]
    print(f"You chose to {chosen_act.task}.")

    if first_input == "1":
        print("Okay let's sleep more...")
        current_time.add_hours(chosen_act.hours)
        current_time.add_minutes(chosen_act.minutes)
        print(f"Now it's {current_time}.  What next?")
        good_morning()

    if first_input == "2":
        print("Wow, great use of your time...")
        current_time.add_hours(chosen_act.hours)
        current_time.add_minutes(chosen_act.minutes)
        print(f"Now it's {current_time}, want to get up now?")
        good_morning()

    if first_input == "3":
        print("Good choice!")
        general_update(chosen_act)
        breakfast_or_not()

def breakfast_or_not():
    if current_time.hours >= 8 or (current_time.hours == 8 and current_time.minutes > 0):
        print("You're late to class.  Do you even want to go still?")
        print(f"Y:  {all_activities[4].task}")
        print(f"N: {all_activities[3].task}")
        first_input = input()
        if first_input == "Y":
            print("Good thing we go to school online...")
            general_update(all_activities[4])
            print(f"Class is over.  It's now {current_time}.  What next?")
            after_class()
        if first_input == "N":
            skipped_class()

    if current_time.hours < 8:    
        print(f"Now it's {current_time}, Do you want to eat some breakfast?")
        print(f"Y: {all_activities[3].task}")
        print(f"N: No I'm not hungry.")
        first_input = input()
        if first_input == "Y":
            general_update(all_activities[3])
            # current_time.add_minutes(all_activities[3].minutes)
            print("Finished eating breakfast.")
            class_or_not()

        if first_input == "N":
            print("Alright then.")
            class_or_not()

def class_or_not():
        print("Alright, class starts at 8:00.  Should we go?")
        print("Y: Yes.")
        print("N: No let's do something fun instead!")
        first_input = input()
        if first_input == "Y":
            current_time.hours = 4
            current_time.minutes = 0
            general_update(all_activities[5])
            print(f"Class is over.  It's now {current_time}.  What next?")
            after_class()
        if first_input == "N":
            skipped_class()


after_class_list = [all_activities[7], all_activities[8], all_activities[12], all_activities[10]]
after_class_inputs = [1, 1, 1, 1]

def after_class():
    print(f"1: {after_class_list[0].task}")
    print(f"2: {after_class_list[1].task}")
    print(f"3: {after_class_list[2].task}")
    print(f"4: {after_class_list[3].task}")
    print("5: I want to do something else now.")
    first_input = input()

    if first_input == "1":
        general_update(after_class_list[0])
        after_class()
        # current_time.add_hours(after_class_list[0].hours)
    if first_input == "2" and after_class_inputs[1] == 1:
        general_update(after_class_list[1])
        # current_time.add_hours(after_class_list[1].hours)
        after_class_inputs[1] = 0
        after_class()
    if first_input == "2" and after_class_inputs[1] == 0:
        print("You just went to the gym!  Choose something else.")
        after_class()
        # after_class_list[1] = "."
    if first_input == "3" and after_class_inputs[2] == 1:
        general_update(after_class_list[2])
        after_class_inputs[2] = 0
        after_class()
        # current_time.add_hours(after_class_list[2].hours)
    if first_input == "3" and after_class_inputs[2] == 0:
        print("You just ate!  Let's do something else.")
        after_class()
    if first_input == "4":
        general_update(after_class_list[3])
        after_class()
        # current_time.add_hours(after_class_list[3].hours)
    if first_input == "5":
        after_after_class()

after_after_list = [all_activities[14], all_activities[15], all_activities[16], all_activities[18]]
after_after_inputs = [1, 1, 1, 1]

def after_after_class():
    print(f"1: {after_after_list[0].task}")
    print(f"2: {after_after_list[1].task}")
    print(f"3: {after_after_list[2].task}")
    print(f"4: {after_after_list[3].task}")
    first_input = input()

    if first_input == "1":
        general_update(after_after_list[0])
        print(f"Playing Wonderwall...")
        after_after_class()
    if first_input == "2" and after_after_inputs[1] == 1:
        general_update(after_after_list[1])
        after_after_inputs[1] = 0
        chosen_friend = choose_friend()
        print(f"You chose {chosen_friend} to go to the movies with. What movie do you want to see?")
        chosen_movie = choose_movie()
        print(f"Great!  Let's check out {chosen_movie}.")
        print("...")
        print("That was a good movie. What now?")
        after_after_class()
    if first_input == "2" and after_after_inputs == 0:
        print("You just got back from the movies!  Choose something else.")
        after_after_class()
    if first_input == "3" and after_after_inputs[2] == 1:
        general_update(after_after_list[2])
        after_after_inputs[2] = 0
        chosen_friend = choose_friend()
        print(f"Cool, {chosen_friend} is down to grab drinks.  Where do you want to go?")
        chosen_bar = choose_bar()
        print(f"Alright, heading to the local {chosen_bar}.")
        print("...")
        print("Well that was fun, what now?")
        after_after_class()
    if first_input == "3" and after_after_inputs[2] == 0:
        print("You just got back from drinking.  Maybe you should eat some food or go to sleep?")
    if first_input == "4":
        print("Alright, let's eat dinner.")
        print("...")
        print("That hit the spot.  It's getting late, do you want to do anything else before bed?")
        post_dinner()

def post_dinner():
    remaining_hours = 6 + (12 - int(current_time.hours))
    remaining_minutes = 30 + (60 - int(current_time.minutes))
    if remaining_minutes >= 60:
        remaining_minutes -= 60
        remaining_hours += 1
    if 12 > current_time.hours > 6:
        print(f"You have {remaining_hours} hours and {remaining_minutes} minutes until you have to wake up tomorrow.  What do you want to do?")
    if 12 <= current_time.hours <= 3:
        print(f"It's getting late. Time for bed. Sorry!")
        go_to_sleep()

    print(f"1: {all_activities[13].task}")
    print(f"2: {all_activities[20].task}")
    print(f"3: {all_activities[19].task}")
    print(f"4: {all_activities[21].task}")
    post_dinner_input = input()
    if post_dinner_input == "1":
        general_update(all_activities[13])
        chosen_video_game = choose_video_game()
        print(f"Okay, let's play {chosen_video_game} for an hour.")
        post_dinner()
    if post_dinner_input == "2":
        general_update(all_activities[20])
        post_dinner()
    if post_dinner_input == "3":
        general_update(all_activities[19])
        post_dinner()
    if post_dinner_input == "4":
        print("Responsible choice.  Getting ready for bed!")
        go_to_sleep()

def choose_video_game():
    print("1: Apex")
    print("2: Call of Duty")
    print("3: Rocket League")
    print("4: PUBG")
    video_game_input = input()

    if video_game_input == "1":
        return "Apex"
    if video_game_input == "2":
        return "Call of Duty"
    if video_game_input == "3":
        return "Rocket League"
    if video_game_input == "4":
        return "PUBG"
    

def skipped_class():
    print("Cool! Now that we have all day, what do you want to do?")
    print(f"1: {all_activities[9].task}")
    print(f"2: {all_activities[14].task}")
    # print(first_input)

movie_list = {"mario": ["Super Mario Bros", "PG", "7.4/10"], "wick": ["John Wick: Chapter 4", "R", "8.2/10"], "beau": ["Beau is Afraid", "R", "7.4/10"], "air": ["Air", "R", "7.7/10"]}

# set_trace()

def choose_friend():
    i = 1
    for friend in all_friends:
        print(f"{i}: {friend.name}")
        i += 1
    second_input = input()
    return all_friends[int(second_input) - 1].name

def choose_movie():
    print(f"1: {movie_list['mario'][0]}  Rating: {movie_list['mario'][1]}  Critic Score: {movie_list['mario'][2]}")
    print(f"2: {movie_list['wick'][0]}  Rating: {movie_list['wick'][1]}  Critic Score: {movie_list['wick'][2]}")
    print(f"3: {movie_list['beau'][0]}  Rating: {movie_list['beau'][1]}  Critic Score: {movie_list['beau'][2]}")
    print(f"4: {movie_list['air'][0]}  Rating: {movie_list['air'][1]}  Critic Score: {movie_list['air'][2]}")
    movie_input = input()

    if movie_input == "1":
        return movie_list['mario'][0]
    if movie_input == "2":
        return movie_list['wick'][0]
    if movie_input == "3":
        return movie_list['beau'][0]
    if movie_input == "4":
        return movie_list['air'][0]
    
def choose_bar():
    print("1: Cocktail Lounge")
    print("2: Sports Bar")
    print("3: Dive Bar")
    print("4: Pool Hall")
    print("5: Brewery")
    bar_input = input()

    if bar_input == "1":
        return "cocktail lounge"
    if bar_input == "2":
        return "sports bar"
    if bar_input == "3":
        return "dive bar"
    if bar_input == "4":
        return "pool hall"
    if bar_input == "5":
        return "brewery"

def go_to_sleep():
    global productivity_score
    print(f"You did a lot today. Some things were super productive, but others not so much. Here's how you did:")
    if productivity_score < 5:
        print("Man you're a bum.")
    if 10 > productivity_score >= 5:
        print("Chill day huh?")
    if 15 > productivity_score >= 10:
        print("Just another day I suppose.")
    if 20 > productivity_score >= 15:
        print("That was a pretty busy day!")
    if 25 > productivity_score >= 20:
        print("Wow! You did a ton today!")
    else:
        print("You must have mastered time travel to be that productive.")

    print("Press any key to go to sleep and start another day...")
    daily_score = Day(productivity = productivity_score)
    session.add(daily_score)
    session.commit()

    end_day_input = input()
    if end_day_input:
        Time(6, 30)
        good_morning()

