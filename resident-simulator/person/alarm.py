"Contains functions for executing functions at a specific time for a specific user."

import datetime as module_datetime

class Alarm(object):
    "Object for executing functions at a specific time for a specific user."
    def __init__(self, datetime, action, person):
        self.datetime = datetime
        self.action = action
        self.person = person

    def update(self, world):
        """Call to compare world's date and time to the set date and time.
        Executes function if time is equal."""
        timediff = self.datetime - world.GetDateTime()
        if timediff.seconds == 0 and timediff.days == 0:
            self.action(self.person)
            del self

    @staticmethod
    def set_next_day(person, action, hours, minutes=0):
        "Sets an alarm for the next day at a given time."
        new_date = person.world.GetDateTime().date() + module_datetime.timedelta(1)
        new_time = module_datetime.time(hours, minutes)
        new_datetime = module_datetime.datetime.combine(new_date, new_time)
        alarm = Alarm(new_datetime, action, person)
        person.world.CreateAlarm(alarm)
        return alarm

    @staticmethod
    def set_today(person, action, hours, minutes=0):
        "Sets an alarm for this day at a given time."
        date = person.world.GetDateTime().date()
        time = module_datetime.time(hours, minutes)
        new_datetime = module_datetime.datetime.combine(date, time)
        alarm = Alarm(new_datetime, action, person)
        person.world.CreateAlarm(alarm)
        return alarm

    @staticmethod
    def set_after_minutes(person, action, minutes):
        "Sets an alarm to be executed after a set amount of minutes."
        new_datetime = person.world.GetDateTime() + module_datetime.timedelta(minutes=minutes)
        alarm = Alarm(new_datetime, action, person)
        person.world.CreateAlarm(alarm)
        return alarm
        