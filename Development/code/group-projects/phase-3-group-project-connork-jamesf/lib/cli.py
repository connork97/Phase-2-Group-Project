from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ipdb import set_trace
from datetime import time, timedelta, datetime

from models import (Base, Day, Friend, Activity)
from helpers import good_morning, current_time, general_commands
from rich.console import Console
from rich.style import Style
console = Console()


if __name__ == '__main__':

    good_morning()