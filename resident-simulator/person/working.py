"Simulates the working action of a person."

from datetime import timedelta
from person.alarm import Alarm
from person.eating import __eat_lunch

#TODO: Implement real time (historic) traffic data to simulate ETA
#TODO: Implement traffic delay based on geolocation

def go_home(person):
    "Simulates going home"
    person.enter_building(person.home)

def work(person):
    "Simulates working."
    person.leave_building()
    person.print_action("goes to work")
    #friday night: extra time on work
    working_time = 10 if person.world.datetime.weekday() == 4 else 9
    homedt = person.world.datetime + timedelta(hours=working_time)
    time_time = homedt.time()
    Alarm.set_today(person, __eat_lunch, 12, 30)
    Alarm.set_today(person, go_home, time_time.hour, time_time.minute)
