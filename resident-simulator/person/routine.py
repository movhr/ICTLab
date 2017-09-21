"Simulates alarm person's daily routine (experimental)"

from datetime import datetime, time
from person.alarm import Alarm

class Routine(object):
    "Simulates alarm person's daily routine (experimental)"
    def __init__(self, person):
        self.alarms = []
        self.person = person

    def create_event(self, func, hour, minute):
        "Creates alarm new event to execute every day."
        new_datetime = datetime.combine(datetime.now().date(), time(hour,minute))
        alarm = Alarm(new_datetime, func, self.person)
        self.alarms.append(alarm)

    def update(self, current_time):
        "Checks if an action must be executed."
        dosomething = False
        for alarm in self.alarms:
            if alarm.datetime.time() == current_time:
                self.person.Do(alarm.func)
                dosomething = True
        return dosomething
