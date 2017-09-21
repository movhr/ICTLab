"World simulator module"

import time
import datetime
from assets.building import Building
from person.simperson import Person
from person.alarm import Alarm
from person.sleeping import wake_with_alarm
from assets.heater import Heater

import masternode

class World(object):
    def __init__(self):
        self.datetime = datetime.datetime(2017, 1, 2, 7) #2017-01-01 06:00 GMT+0
        self.minutesPerSecond = 3
        self.buildings = []
        self.people = []
        self.outsideTemperature = 15 #degrees celcius
        self.alarms = []

    def CreatePerson(self, name, home):
        newPerson = Person(name, home, self)
        self.people.append(newPerson)
        self.CreateAlarm(Alarm(datetime.datetime(2017, 1, 2, 7, 30), wake_with_alarm, newPerson))
        return newPerson

    def CreateBuilding(self, name):
        newBuilding = Building(name, self)
        self.buildings.append(newBuilding)
        return newBuilding

    def CreateAlarm(self, alarm):
        self.alarms.append(alarm)

    def TryRemoveAlarm(self, alarm):
        try:
            self.alarms.remove(alarm)
            return True
        except ValueError:
            return False

    def __update(self):

        masternode.updateDatabase()

        for a in self.alarms:
            a.update(self)

        for p in self.people:
            p.update()

        for b in self.buildings:
            b.update()

        self.datetime += datetime.timedelta(minutes=1)

    def Simulate(self):
        "Simulates the current world."
        while True:
            time.sleep(1/self.minutesPerSecond)
            self.__update()

            if self.datetime.minute == 0:
                for p in self.people:
                    p.sitrep()

                for b in self.buildings:
                    b.update_usage_levels()

    def GetTime(self):
        return self.datetime.time()

    def GetDateTime(self):
        return self.datetime

    def TimeUntil(self, time):
        d = self.datetime.date()
        odt = datetime.datetime.combine(d, time)
        return odt - self.datetime

    def IsTomorrowWeekDay(self):
        newDate = self.datetime + datetime.timedelta(1)
        return newDate.weekday() < 5

    def IsTodayWeekday(self):
        return self.datetime.weekday() < 5

    def IsNowBetween(self, hour1, minute1, hour2, minute2):
        d = self.datetime.date()
        t1 = datetime.time(hour1, minute1)
        t2 = datetime.time(hour2, minute2)
        return self.datetime.time() > t1 and self.datetime.time() < t2

    def GetState(self):
        blist = []
        for building in self.buildings:
            building_state = building.collect_usage_levels()
            blist.append({
                'time': str(self.GetDateTime()),
                'building_name': building.name,
                'rooms': building_state,
                'variables': building.collect_building_variables()
            })

        return blist
