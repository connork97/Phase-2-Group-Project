from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import (Base, Friend, Activity, Day)
import random
from ipdb import set_trace
from rich import print
from rich.console import Console
from rich.style import Style
from rich.layout import Layout
from rich.padding import Padding
from rich.align import Align

console = Console()
layout = Layout()

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

layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)

layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)

title = Align.center('''                                              
      /\       |‾‾\     /\    \ /      |  |\  |      ‾‾|‾‾  |   |  |‾‾‾      |    |  |‾‾‾  |‾‾‾
     /__\      |   |   /__\    |       |  | \ |        |    |---|  |--       |    |  |--   |--
    /    \     |__/   /    \   |       |  |  \|        |    |   |  |___      |__  |  |     |___
''')

current_time = Time(6, 30)

instructions = Align.center(f'''
Good morning! It's currently {current_time} and we're going to start our day.
As you go about your day, you'll have various options to choose from
depending on what you've done up to that point.
Some choices are responsible and productive, while others are not.
Choose wisely!
''')
                            
commands = Align.center(f'''
Here's a list of available commands:
------------------------------------
'time' => See the current time.
'today' => See what day of the week it is.
'productivity' => See your 'productivity score' so far today. An average day is in the 10-15 range.
'yesterday' => Find how productive you were yesterday.
'average' => See how productive you are on an average day.
'most' => See your most productive day.
'least' => See your least productive day.
'restart' => Restart your current day.
''')

layout["upper"].update(
    Padding(title, (5, 0, 0, 0), style="white")
)
layout["left"].update(
    instructions
)
layout["right"].update(
    commands
)
print(layout)

console.print(f"Good morning! The current time is {current_time}.", style="spring_green3")

console.print("What are you going to do first?", style="spring_green3")

all_activities = session.query(Activity).all()
all_friends = session.query(Friend).all()
all_days = session.query(Day).all()

productivity_score = 0

days_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}

def day_of_week(n):
    day_num = (n - 1) % 7 + 1
    return days_dict[day_num]

def how_productive(score):
    if score < 5:
        return "very lazy."
    if 10 > score >= 5:
        return "pretty chill."
    if 15 > score >= 10:
        return "fairly productive."
    if 20 > score >= 15:
        return "quite productive."
    if 25 > score >= 20:
        return "really busy!"
    if score >= 25:
        return "insanely productivy!"
    

def general_commands(user_command):
    
    if user_command == "help":
        print(Align.left(commands))

    elif user_command == "time":
        console.print(f"The current time is {current_time}", style="bright_cyan")

    elif user_command == "productivity":
        global productivity_score
        console.print(f"Today's producitivty score so far is: {productivity_score}.", style="bright_cyan")

    elif user_command == "today":
        day_id = session.query(Day.id).order_by(Day.id.desc()).first()
        today = day_of_week(day_id[0] + 1)
        console.print(f"Today is {today}.", style="bright_cyan")

    elif user_command == "yesterday":
        yesterday_id = session.query(Day.id).order_by(Day.id.desc()).first()
        yesterday_prod = session.query(Day.productivity).order_by(Day.id.desc()).first()
        yesterday = day_of_week(yesterday_id[0])
        yesterday_description = how_productive(yesterday_prod[0])
        console.print(f"Yesterday was {yesterday} and it was {yesterday_description}", style="bright_cyan")

    elif user_command == "average":
        all_productivity = session.query(Day.productivity).all()
        total = 0
        for product in all_productivity:
            total += product[0]
        average_productivity = how_productive(total / len(all_productivity))
        console.print(f"On average, your days are {average_productivity}", style="bright_cyan")

    elif user_command == "most":
        most_prod_day = session.query(Day).order_by(Day.productivity.desc()).first()
        # print(most_prod_day.id, most_prod_day.productivity)
        day_name = day_of_week(most_prod_day.id)
        day_prod = how_productive(most_prod_day.productivity)
        console.print(f"Your most productive day was a {day_name} and it was {day_prod}", style="bright_cyan")

    elif user_command == "least":
        most_prod_day = session.query(Day).order_by(Day.productivity).first()
        # print(most_prod_day.id, most_prod_day.productivity)
        day_name = day_of_week(most_prod_day.id)
        day_prod = how_productive(most_prod_day.productivity)

        console.print(f"Your least productive day was a {day_name} and it was {day_prod}", style="bright_cyan")
    elif user_command == "restart":
        go_to_sleep()

    else:
        console.print("Not a valid command.", style="bright_red")

def general_update(chosen_act):

    global productivity_score
    current_time.add_hours(chosen_act.hours)
    current_time.add_minutes(chosen_act.minutes)
    productivity_score += chosen_act.productivity

def good_morning():

    print(f"1: {all_activities[0].task}")
    print(f"2: {all_activities[1].task}")
    print(f"3: {all_activities[2].task}")

    global productivity_score
    productivity_score = 0
    first_input = input()

    if first_input == "1":
        console.print("Okay let's sleep more...", style="bright_red")
        general_update(all_activities[0])
        console.print(f"Now it's {current_time}.  What next?", style="spring_green3")
        good_morning()

    elif first_input == "2":
        console.print("Gotta stay up to date with Instagram...", style="bright_red")
        general_update(all_activities[1])
        console.print(f"Now it's {current_time}, want to get up now?", style="spring_green3")
        good_morning()

    elif first_input == "3":
        console.print("Good choice!", style="bright_cyan")
        general_update(all_activities[2])
        breakfast_or_not()

    else:
        general_commands(first_input)
        good_morning()

def breakfast_or_not():

    global current_time
    if current_time.hours >= 8 or (current_time.hours == 8 and current_time.minutes > 0):
        console.print(f"It's {current_time} and you're late to class.  Do you even want to go still?", style="spring_green3")
        print(f"Y: {all_activities[4].task}")
        print(f"N: No I'll just eat my breakfast and relax.")
        first_input = input()

        if first_input == "Y":
            console.print("Good thing we go to school online...", style="bright_cyan")
            current_time = Time(4, 0)
            console.print(f"Class is over.  It's now {current_time}.  What next?", style="spring_green3")
            after_class()

        elif first_input == "N":
            console.print("Cool! Now that we have all day, what do you want to do?", style="spring_green3")
            skipped_class()

        else:
            general_commands(first_input)
            breakfast_or_not()

    if current_time.hours < 8:
        console.print(f"Now it's {current_time}, Do you want to eat some breakfast?", style="spring_green3")
        print(f"Y: {all_activities[3].task}")
        print(f"N: No I'm not hungry.")
        first_input = input()
        
        if first_input == "Y":
            general_update(all_activities[3])
            console.print("Finished eating breakfast.", style="spring_green3")
            console.print("Alright, class starts at 8:00.  Should we go?", style="spring_green3")
            class_or_not()

        elif first_input == "N":
            console.print("Alright then.", style="spring_green3")
            class_or_not()

        else:
            general_commands(first_input)
            breakfast_or_not()

def class_or_not():
        
        print("Y: Yes.")
        print("N: No let's do something fun instead!")
        first_input = input()

        if first_input == "Y":
            current_time.hours = 4
            current_time.minutes = 0
            general_update(all_activities[5])
            console.print(f"Class is over.  It's now {current_time}.  What next?", style="bright_cyan")
            after_class()
        elif first_input == "N":
            console.print("Cool! Now that we have all day, what do you want to do?", style="bright_cyan")
            skipped_class()
        else:
            general_commands(first_input)
            class_or_not()

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
        console.print("Responsible choice! What next?", style="bright_cyan")
        after_class()

    elif first_input == "2" and after_class_inputs[1] == 1:
        general_update(after_class_list[1])
        after_class_inputs[1] = 0
        console.print("Time for some endorphins!", style="bright_cyan")
        after_class()
    elif first_input == "2" and after_class_inputs[1] == 0:
        console.print("You just went to the gym!  Choose something else.", style="bright_red")
        after_class()

    elif first_input == "3" and after_class_inputs[2] == 1:
        general_update(after_class_list[2])
        console.print("Mmmm...", style="bright_cyan")
        after_class_inputs[2] = 0
        after_class()
    elif first_input == "3" and after_class_inputs[2] == 0:
        console.print("You just ate!  Let's do something else.", style="bright_red")
        after_class()

    elif first_input == "4":
        general_update(after_class_list[3])
        console.print("Shoutout to Phil", style="bright_cyan")
        after_class()

    elif first_input == "5":
        console.print("Cool, what's next?", style="spring_green3")
        after_after_class()
    else:
        general_commands(first_input)
        after_class()

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
        console.print(f"Playing Wonderwall...", style="bright_cyan")
        after_after_class()

    elif first_input == "2" and after_after_inputs[1] == 1:
        general_update(after_after_list[1])
        after_after_inputs[1] = 0
        console.print("Who do you want to see a movie with?", style="spring_green3")
        chosen_friend = choose_friend()
        console.print(f"You chose {chosen_friend} to go to the movies with. What movie do you want to see?", style="spring_green3")
        chosen_movie = choose_movie()
        console.print(f"Great!  Let's check out {chosen_movie}.", style="bright_cyan")
        print("...")
        console.print("That was a good movie. What now?", style="spring_green3")
        after_after_class()
    elif first_input == "2" and after_after_inputs[1] == 0:
        console.print("You just got back from the movies!  Choose something else.", style="bright_red")
        after_after_class()

    elif first_input == "3" and after_after_inputs[2] == 1:
        general_update(after_after_list[2])
        after_after_inputs[2] = 0
        console.print("Who do you want to grab drinks with?", style="spring_green3")
        chosen_friend = choose_friend()
        console.print(f"Cool, {chosen_friend} is down to grab drinks.  Where do you want to go?", style="spring_green3")
        chosen_bar = choose_bar()
        console.print(f"Alright, heading to the local {chosen_bar}.", style="bright_cyan")
        print("...")
        console.print("Well that was fun, what now?", style="spring_green3")
        after_after_class()
    elif first_input == "3" and after_after_inputs[2] == 0:
        console.print("You just got back from drinking.  Maybe you should eat some food or go to sleep?", style="bright_red")
        after_after_class()

    elif first_input == "4":
        console.print("Alright, let's eat dinner.", style="bright_cyan")
        print("...")
        console.print("That hit the spot.  It's getting late, do you want to do anything else before bed?", style="spring_green3")
        post_dinner()
    else:
        general_commands(first_input)
        after_after_class()

def post_dinner():
    remaining_hours = 5 + (12 - int(current_time.hours))
    remaining_minutes = 30 + (60 - int(current_time.minutes))

    if remaining_minutes >= 60:
        remaining_minutes -= 60
        remaining_hours += 1
    if 12 > current_time.hours > 6:
        console.print(f"You have {remaining_hours} hours and {remaining_minutes} minutes until you have to wake up tomorrow.  What do you want to do?", style="spring_green3")
    if 12 <= current_time.hours <= 3:
        console.print(f"It's getting late. Time for bed. Sorry!", style="bright_red")
        go_to_sleep()

    print(f"1: {all_activities[13].task}")
    print(f"2: {all_activities[20].task}")
    print(f"3: {all_activities[19].task}")
    print(f"4: {all_activities[21].task}")
    post_dinner_input = input()

    if post_dinner_input == "1":
        general_update(all_activities[13])
        chosen_video_game = choose_video_game()
        console.print(f"Okay, let's play {chosen_video_game} for an hour.", style="bright_cyan")
        post_dinner()
    elif post_dinner_input == "2":
        general_update(all_activities[20])
        console.print("Alright, who dies next in Game of Thrones...", style="bright_cyan")
        post_dinner()
    elif post_dinner_input == "3":
        general_update(all_activities[19])
        console.print("Good thing my buddy gave me his Netflix password.", style="bright_cyan")
        post_dinner()
    elif post_dinner_input == "4":
        console.print("Responsible choice.  Getting ready for bed!", style="bright_cyan")
        go_to_sleep()
    else:
        general_commands(post_dinner_input)
        post_dinner()

def choose_video_game():
    console.print("What do you want to play?", style="spring_green3")
    print("1: Apex")
    print("2: Call of Duty")
    print("3: Rocket League")
    print("4: PUBG")
    video_game_input = input()

    if video_game_input == "1":
        return "Apex"
    elif video_game_input == "2":
        return "Call of Duty"
    elif video_game_input == "3":
        return "Rocket League"
    elif video_game_input == "4":
        return "PUBG"
    else:
        general_commands(video_game_input)
        post_dinner()

skipped_class_inputs = [1, 1, 1, 1]

def skipped_class():
    print(f"1: {all_activities[9].task}")
    print(f"2: {all_activities[23].task}")
    print(f"3: {all_activities[24].task}")
    print(f"4: {all_activities[25].task}")
    print(f"5: Let's move on with our day.")
    skipped_input = input()

    if skipped_input == "1" and skipped_class_inputs[0] == 1:
        console.print("It's a lovely day for a hike. Let's go!", style="bright_cyan")
        general_update(all_activities[9])
        skipped_class_inputs[0] = 0
        skipped_class()
    elif skipped_input == "1" and skipped_class_inputs[0] == 0:
        console.print("You just got back from a hike! Try something else.", style="bright_red")
        skipped_class()

    elif skipped_input == "2"and skipped_class_inputs[1] == 1:
        general_update(all_activities[23])
        console.print("Don't forget your harness!", style="bright_cyan")
        skipped_class_inputs[1] = 0
        skipped_class()
    elif skipped_input == "2" and skipped_class_inputs[1] == 0:
        console.print("You just finished climbing! Try something else.", style="bright_red")
        skipped_class()
    
    elif skipped_input == "3" and skipped_class_inputs[2] == 1:
        console.print("Who do you want to go to brunch with?", style="spring_green3")
        general_update(all_activities[24])
        skipped_class_inputs[2] = 0
        chosen_friend = choose_friend()
        console.print(f"Let's get some mimosas with {chosen_friend}", style="bright_cyan")
        skipped_class()
    elif skipped_input == "3" and skipped_class_inputs[2] == 0:
        console.print("Let's do something other than brunch now...", style="bright_red")
        skipped_class()
    
    elif skipped_input == "4" and skipped_class_inputs[3] == 1:
        general_update(all_activities[25])   
        console.print("Let's go Tiger!", style="bright_cyan")
        skipped_class_inputs[3] = 0
        skipped_class()
    elif skipped_input == "4" and skipped_class_inputs[3] == 0:
        console.print("You just played 18 holes. That's enough for today.", style="bright_red")
        skipped_class()
    
    elif skipped_input == "5":
        afternoon_activities()

    else:
        general_commands(skipped_input)
        skipped_class()

def afternoon_activities():
    console.print(f"It's {current_time} now. Let's do something a bit more productive for while.", style="spring_green3")
    print(f"1: {all_activities[6].task}")
    print(f"2: {all_activities[26].task}")
    print(f"3: {all_activities[27].task}")
    print(f"4: Let's think of something else to do now.")
    afternoon_input = input()

    if afternoon_input == "1":
        console.print(f"Good idea. To be honest it's been a bit of a mess around here lately...", style="bright_cyan")
        general_update(all_activities[6])
        afternoon_activities()
    elif afternoon_input == "2":
        console.print("Make sure you eat something first!", style="bright_cyan")
        general_update(all_activities[26])
        afternoon_activities()
    elif afternoon_input == "3":
        console.print("Nice, that pile of clothes has been there a while...", style="bright_cyan")
        general_update(all_activities[27])
        afternoon_activities()
    elif afternoon_input == "4":
        console.print("Do you feel like organizing a game night with a few friends?", style="spring_green3")
        print("Y: Definitely!")
        print("N: Not in the mood.")
        game_input = input()
        if game_input == "Y":
            general_update(all_activities[17])
            console.print("Awesome! Let's find a few friends to invite!", style="bright_cyan")
            game_night()
        elif game_input == "N":
            console.print("No problem, let's find something else to do.", style="bright_cyan")
            after_after_class()
        else:
            general_commands(afternoon_input)
            afternoon_activities()
    else:
        general_commands(afternoon_input)
        afternoon_activities()
    
def game_night():
    friends_list = ["you"]

    while len(friends_list) < 4:
        console.print(f"Invite {4 - len(friends_list)} more friends to play.", style="spring_green3")
        friend = choose_friend()
        if friend not in friends_list:
            friends_list.append(friend)
        elif friend in friends_list:
            console.print(f"You've already invited {friend}. Choose someone else!", style="bright_red")
    
    console.print("Now that we've invited a few friends to play, let's pick out a game!", style="spring_green3")
    chosen_game = choose_game()
    console.print(f"{chosen_game} is so much fun! Good choice!", style="bright_cyan")
    console.print(f"...", style="spring_green3")
    console.print(f"Congrats to {random.choice(friends_list)} for winning {chosen_game}!", style="bright_cyan")
    post_dinner()

def choose_game():
    print("1: Catan")
    print("2: Monopoly")
    print("3: Cards Against Humanity")
    print("4: Poker")
    chosen_game_input = input()

    if chosen_game_input == "1":
        return "Catan"
    elif chosen_game_input == "2":
        return "Monopoly"
    elif chosen_game_input == "3":
        return "Cards Against Humanity"
    elif chosen_game_input == "4":
        return "Poker"    
    else:
        general_commands(chosen_game_input)
        game_night()
    
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
    elif movie_input == "2":
        return movie_dict['wick'][0]
    elif movie_input == "3":
        return movie_dict['beau'][0]
    elif movie_input == "4":
        return movie_dict['air'][0]
    else:
        general_commands(movie_input)
        after_after_class()

def choose_bar():
    print("1: Cocktail Lounge")
    print("2: Sports Bar")
    print("3: Dive Bar")
    print("4: Pool Hall")
    print("5: Brewery")
    bar_input = input()

    if bar_input == "1":
        return "cocktail lounge"
    elif bar_input == "2":
        return "sports bar"
    elif bar_input == "3":
        return "dive bar"
    elif bar_input == "4":
        return "pool hall"
    elif bar_input == "5":
        return "brewery"
    else:
        general_commands(bar_input)
        after_after_class()

def go_to_sleep():
    global productivity_score
    console.print(f"You did a lot today. Some things were super productive, but others not so much. Here's how you did:", style="spring_green3")
    if productivity_score < 5:
        console.print("Man you're a bum.", style="bright_red")
    if 10 > productivity_score >= 5:
        console.print("Chill day huh?", style="bright_red")
    if 15 > productivity_score >= 10:
        console.print("Just another day I suppose.", style="bright_cyan")
    if 20 > productivity_score >= 15:
        console.print("That was a pretty busy day!", style="bright_cyan")
    if 25 > productivity_score >= 20:
        console.print("Wow! You did a ton today!", style="bright_cyan")
    if productivity_score > 25:
        console.print("You must have mastered time travel to be that productive.", style="bright_cyan")

    console.print("Press any key to go to sleep and start another day...", style="spring_green3")
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
    for i in skipped_class_inputs:
        if i != 1:
            i = 1

    end_day_input = input()
    if end_day_input:
        global current_time
        current_time = Time(6, 30)
        good_morning()

