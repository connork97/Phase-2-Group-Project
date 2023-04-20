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

for activity in all_activities:
    print(activity.task, activity.hours, activity.minutes, activity.id)


def good_morning():

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
        current_time.add_hours(chosen_act.hours)
        current_time.add_minutes(chosen_act.minutes)
        breakfast_or_not()

def breakfast_or_not():
    if current_time.hours >= 8 or (current_time.hours == 8 and current_time.minutes > 0):
        print("You're late to class.  Do you even want to go still?")
        print(f"Y:  {all_activities[4].task}")
        print(f"N: {all_activities[3].task}")
        first_input = input()
        
        if first_input == "Y":
            print("Good thing we go to school online...")
            after_class()
        if first_input == "N":
            skipped_class()

    if current_time.hours < 8:    
        print(f"Now it's {current_time}, Do you want to eat some breakfast?")
        print(f"Y: {all_activities[3].task}")
        print(f"N: No I'm not hungry.")
        first_input = input()
        if first_input == "Y":
            current_time.add_minutes(all_activities[3].minutes)
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
            after_class()
        if first_input == "N":
            skipped_class()


after_class_list = [all_activities[7], all_activities[8], all_activities[11], all_activities[10]]
after_class_inputs = [1, 1, 1, 1]

def after_class():
    print(f"Class is over.  It's now {current_time}.  What next?")
    print(f"1: {after_class_list[0].task}")
    print(f"2: {after_class_list[1].task}")
    print(f"3: {after_class_list[2].task}")
    print(f"4: {after_class_list[3].task}")
    first_input = input()

    if first_input == "1":
        current_time.add_hours(after_class_list[0].hours)
    if first_input == "2" and after_class_inputs[1] == 1:
        current_time.add_hours(after_class_list[1].hours)
        after_class_inputs[1] = 0
        # del after_class_list[1]
        # after_class_list.append("You already went to the gym.")
        # set_trace()
        after_class()
        # after_class_list[1] = "."
    if first_input == "3":
        current_time.add_hours(after_class_list[2].hours)
    if first_input == "4":
        current_time.add_hours(after_class_list[3].hours)



    print(first_input)

def skipped_class():
    print("Cool! Now that we have all day, what do you want to do?")
    print(f"1: {all_activities[9].task}")
    print(f"2: {all_activities[13].task}")
    # print(first_input)
    
    
