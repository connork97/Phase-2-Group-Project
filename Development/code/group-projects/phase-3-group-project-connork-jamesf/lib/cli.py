from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ipdb import set_trace
from datetime import time, timedelta, datetime

from models import (Base, Day, Friend, Activity)
from helpers import good_morning, current_time




if __name__ == '__main__':

    print(f"Good morning! The current time is {current_time}.")

    print("What are you going to do first?")

    good_morning()