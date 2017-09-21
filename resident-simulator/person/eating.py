"Module for simulating eating."

import datetime
from random import Random
from enum import Enum
from person.alarm import Alarm
from person.action import ExecutionType
from assets.stove import Stove
from room.kitchen import Kitchen
from room.livingroom import LivingRoom

# accepted snack time before a meal is 1 hour and 30 minutes
ASTBM = datetime.timedelta(hours=1, minutes=30)
def breakfast_time(world): return datetime.time(8, 30) if world.IsTodayWeekday() else datetime.time(10, 30)
def lunch_time(world): return datetime.time(12, 30) if world.IsTodayWeekday() else datetime.time(14, 0)
def dinner_time(world): return datetime.time(18) if world.IsTodayWeekday() else datetime.time(19,15)

class Mealtypes(Enum):
    "Enum for types of meals."
    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2
    SNACK = 3

    @staticmethod
    def Get(world):
        bt = world.TimeUntil(breakfast_time(world))
        lt = world.TimeUntil(lunch_time(world))
        dt = world.TimeUntil(dinner_time(world))


        if bt <= ASTBM and bt.days == 0:
            return Mealtypes.BREAKFAST
        elif lt <= ASTBM and lt.days == 0:
            return Mealtypes.LUNCH
        elif dt <= ASTBM and dt.days == 0:
            return Mealtypes.DINNER
        else:
            return Mealtypes.SNACK

#Snacking
def __eat_snack(person):
    person.hunger -= 60
    person.toilet += 15
    person.print_action("eats a snack")

#Meals
def __eat_breakfast(person):
    person.hunger = 0
    person.toilet += 30
    person.print_action("eats breakfast")

def __eat_lunch(person):
    person.hunger = 0
    person.toilet += 50
    person.print_action("eats lunch")

def __eat_dinner(person):
    person.hunger = 0
    person.toilet += 60
    person.print_action("eats dinner")

def __turnoff_stove(person):
    person.print_action("turns off the stove")
    person.current_room.find_sim_object(Stove).deactivate()

enter_livingroom = lambda person: person.entered_building.enter_room(LivingRoom, person)

def __cook_meal(person, stove_chance, stove_time, waiting_time):
    kitchen = person.entered_building.enter_room(Kitchen, person)
    person.print_action("is cooking for " + str(waiting_time) + " minutes.")
    use_stove = Random().randint(0, 100) <= stove_chance
    if use_stove:
        stove_time = int(waiting_time * (float(stove_time) / 100))
        person.print_action("uses the stove for " + str(stove_time) + " minutes.")
        kitchen.find_sim_object(Stove).activate()
        Alarm.set_after_minutes(person, __turnoff_stove, stove_time)


# Generic eat function
# should be expanded more, therefore it has now the same body
def eat(person):
    "Simulates an eating action."
    meal_type = Mealtypes.Get(person.world)
    if meal_type == Mealtypes.BREAKFAST:
        person.print_action("prepares breakfast")
        waiting_time = Random().randint(2, 10)
        person.act(lambda p: __cook_meal(p, 10, 20, waiting_time), waiting_time, exectype = ExecutionType.BEFORE_EXECUTIONTIME) 
        person.act(enter_livingroom, 0)
        person.act(__eat_breakfast, 5, 10)
    elif meal_type == Mealtypes.LUNCH:
        person.print_action("prepares lunch")
        waiting_time = Random().randint(10, 20)
        person.act(lambda p: __cook_meal(p, 50, 70, waiting_time), waiting_time, exectype = ExecutionType.BEFORE_EXECUTIONTIME)
        person.act(enter_livingroom, 0)
        person.act(__eat_lunch, 10, 20)
    elif meal_type == Mealtypes.DINNER:
        person.print_action("prepares dinner")
        waiting_time = Random().randint(15, 60)
        person.act(lambda p: __cook_meal(p, 80, 80, waiting_time), waiting_time, exectype = ExecutionType.BEFORE_EXECUTIONTIME)
        person.act(enter_livingroom, 0)
        person.act(__eat_dinner, 15, 30)
    else:
        person.print_action("prepares a snack")
        person.act(__eat_snack, 0, 5)

