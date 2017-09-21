"Simulates sleeping action."

from random import Random
from person.alarm import Alarm
from room.bedroom import Bedroom
from person.action import ExecutionType
from person.sanitary import use_shower

TIME_SLEPT = 0
SLEEPING_ACTION = None
WAKE_ALARM = None
WAKE_NO_ALARM = None

def __wakeup(person):
    global TIME_SLEPT
    person.print_action("wakes up")
    person.current_room.turn_on_lights()
    person.entered_building.turn_on_heater()
    person.is_sleeping = False
    if person.tiredness < 60:
        person.tiredness = Random().randint(30, 90)
    person.print_action("has slept for " + str(TIME_SLEPT/60) + " hours and " + str(TIME_SLEPT % 60) + " minutes.")
    TIME_SLEPT = 0
    use_shower(person)

def wake_with_alarm(person):
    global SLEEPING_ACTION
    global WAKE_NO_ALARM
    if WAKE_NO_ALARM:
        person.action_queue.remove(WAKE_NO_ALARM)
        WAKE_NO_ALARM = None
    if SLEEPING_ACTION:
        person.action_queue.remove(SLEEPING_ACTION)
        SLEEPING_ACTION = None
    __wakeup(person)

def wake_before_alarm(person):
    global WAKE_ALARM
    person.world.TryRemoveAlarm(WAKE_ALARM)
    WAKE_ALARM = None
    __wakeup(person)

def __nothing(person):
    person.fun += 5
    person.tiredness -= 2
    return

def __sleep(person):
    global TIME_SLEPT
    person.tiredness -= 2
    TIME_SLEPT += 1

def sleep(person):
    "Lets a person sleep until fully rested or alarm goes off."
    global WAKE_ALARM
    global WAKE_NO_ALARM
    global SLEEPING_ACTION
    person.print_action("goes to bed")
    person.entered_building.turn_off_heater()
    person.entered_building.enter_room(Bedroom, person)
    person.current_room.keep_on_lights(1)
    person.act(__nothing, 15, 25, ExecutionType.CONTINUOUS)

    # sleep for a maximum of 10 hours
    SLEEPING_ACTION = person.act(__sleep, 60*10, exectype=ExecutionType.CONTINUOUS)
    person.current_room.turn_off_lights()
    person.is_sleeping = True

    # Queue wake if time slept reaches 12 hours
    # Else wake by alarm
    WAKE_NO_ALARM = person.act(wake_before_alarm)
    WAKE_ALARM = Alarm.set_next_day(person, wake_with_alarm,
                                    8 if person.world.IsTomorrowWeekDay() else 10)
