from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (Base, Friend, Activity, Day)
import random


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

# for activity in all_activities:
#     print(activity.task, activity.hours, activity.minutes, activity.id)

# days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# days_index = 0

productivity_score = 0

# general_input = input()
# if general_input == "see productivity":
#     print(productivity_score)


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

    if first_input == "1":
        print("Okay let's sleep more...")
        general_update(chosen_act)
        print(f"Now it's {current_time}.  What next?")
        good_morning()

    if first_input == "2":
        print("Wow, great use of your time...")
        general_update(chosen_act)
        print(f"Now it's {current_time}, want to get up now?")
        good_morning()

    if first_input == "3":
        print("Good choice!")
        general_update(chosen_act)
        breakfast_or_not()

def breakfast_or_not():
    if current_time.hours >= 8 or (current_time.hours == 8 and current_time.minutes > 0):
        print(f"It's {current_time} and you're late to class.  Do you even want to go still?")
        print(f"Y: {all_activities[4].task}")
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
            print("Cool! Now that we have all day, what do you want to do?")
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
    
skipped_class_inputs = [1, 1, 1, 1]

def skipped_class():
    print(f"1: {all_activities[9].task}")
    print(f"2: {all_activities[23].task}")
    print(f"3: {all_activities[24].task}")
    print(f"4: {all_activities[25].task}")
    print(f"5: Let's move on with our day.")
    skipped_input = input()

    if skipped_input == "1" and skipped_class_inputs[0] == 1:
        print("It's a lovely day for a hike. Let's go!")
        general_update(all_activities[9])
        skipped_class_inputs[0] = 0
        skipped_class()
    if skipped_input == "1" and skipped_class_inputs[0] == 0:
        print("You just got back from a hike! Try something else.")
    
    if skipped_input == "2"and skipped_class_inputs[1] == 1:
        general_update(all_activities[23])
        print("Don't forget your harness!")
        skipped_class_inputs[1] = 0
        skipped_class()
    if skipped_input == "2" and skipped_class_inputs[1] == 0:
        print("You just finished climbing! Try something else.")
        skipped_class()
    
    if skipped_input == "3" and skipped_class_inputs[2] == 1:
        print("Who do you want to go to brunch with?")
        general_update(all_activities[24])
        skipped_class_inputs[2] = 0
        chosen_friend = choose_friend()
        print(f"Let's get some mimosas with {chosen_friend}")
        skipped_class()
    if skipped_input == "3" and skipped_class_inputs[2] == 0:
        print("Let's do something other than brunch now...")
        skipped_class()
    
    if skipped_input == "4" and skipped_class_inputs[3] == 1:
        general_update(all_activities[25])   
        print("Let's go Tiger!")
        skipped_class_inputs[3] = 0
        skipped_class()
    if skipped_input == "4" and skipped_class_inputs[3] == 0:
        print("You just played 18 holes. That's enough for today.")
        skipped_class()
    
    if skipped_input == "5":
        print(current_time)
        afternoon_activities()        

def afternoon_activities():
    print(f"It's {current_time} now. Let's do something a bit more productive for while.")
    print(f"1: {all_activities[6].task}")
    print(f"2: {all_activities[26].task}")
    print(f"3: {all_activities[27].task}")
    print(f"4: Let's think of something else to do now.")
    afternoon_input = input()

    if afternoon_input == "1":
        print(f"It's been a bit of a mess around here honestly...")
        general_update(all_activities[6])
        afternoon_activities()
    if afternoon_input == "2":
        print("Make sure you eat something first.")
        general_update(all_activities[26])
        afternoon_activities()
    if afternoon_input == "3":
        print("That pile of clothes has been there a while...")
        general_update(all_activities[27])
        afternoon_activities()
    if afternoon_input == "4":
        print("Do you feel like organizing a game night with a few friends?")
        print("Y: Definitely!")
        print("N: Not in the mood.")
        game_input = input()
        if game_input == "Y":
            game_night()
        if game_input == "N":
            after_after_class()
    
def game_night():
    friends_list = ["you"]

    while len(friends_list) < 4:
        print(f"Invite {4 - len(friends_list)} more friends to play.")
        friend = choose_friend()
        if friend not in friends_list:
            friends_list.append(friend)
        elif friend in friends_list:
            print(f"You've already invited {friend}. Choose someone else!")
    
    print("Now that we've invited a few friends to play, let's pick out a game!")
    chosen_game = choose_game()
    print(f"{chosen_game} is so much fun! Good choice!")
    print(f"...")
    print(f"Congrats to {random.choice(friends_list)} for winning {chosen_game}!")
    post_dinner()

def choose_game():
    print("1: Catan")
    print("2: Monopoly")
    print("3: Cards Against Humanity")
    print("4: Poker")
    chosen_game_input = input()

    if chosen_game_input == "1":
        return "Catan"
    if chosen_game_input == "2":
        return "Monopoly"
    if chosen_game_input == "3":
        return "Cards Against Humanity"
    if chosen_game_input == "4":
        return "Poker"    

    
    # friend1 = choose_friend()
    # friends_list.append(friend1)
    # friend2 = choose_friend()
    # friends_list.append(friend2)
    # friend3 = choose_friend()
    # friends_list.append(friend3)
        
movie_dict = {"mario": ["Super Mario Bros", "PG", "7.4/10"], "wick": ["John Wick: Chapter 4", "R", "8.2/10"], "beau": ["Beau is Afraid", "R", "7.4/10"], "air": ["Air", "R", "7.7/10"]}

def choose_friend():
    i = 1
    for friend in all_friends:
        print(f"{i}: {friend.name}")
        i += 1
    second_input = input()
    return all_friends[int(second_input) - 1].name

def choose_movie():
    print(f"1: {movie_dict['mario'][0]}  Rating: {movie_dict['mario'][1]}  Critic Score: {movie_dict['mario'][2]}")
    print(f"2: {movie_dict['wick'][0]}  Rating: {movie_dict['wick'][1]}  Critic Score: {movie_dict['wick'][2]}")
    print(f"3: {movie_dict['beau'][0]}  Rating: {movie_dict['beau'][1]}  Critic Score: {movie_dict['beau'][2]}")
    print(f"4: {movie_dict['air'][0]}  Rating: {movie_dict['air'][1]}  Critic Score: {movie_dict['air'][2]}")
    movie_input = input()

    if movie_input == "1":
        return movie_dict['mario'][0]
    if movie_input == "2":
        return movie_dict['wick'][0]
    if movie_input == "3":
        return movie_dict['beau'][0]
    if movie_input == "4":
        return movie_dict['air'][0]
    
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
    if productivity_score > 25:
        print("You must have mastered time travel to be that productive.")

    print("Press any key to go to sleep and start another day...")
    daily_score = Day(productivity = productivity_score)
    session.add(daily_score)
    session.commit()

    global after_class_inputs
    for i in after_class_inputs:
        if i != 1:
            i = 1
    for i in after_after_inputs:
        if i != 1:
            i = 1

    end_day_input = input()
    if end_day_input:
        global current_time
        current_time = Time(6, 30)
        good_morning()

