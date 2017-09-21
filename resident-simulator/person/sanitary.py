"Contains function for interacting with the bathroom."

from room.bathroom import Bathroom
from assets.toilet import Toilet
from assets.shower import Shower
from assets.bath import Bath

from person.alarm import Alarm
from person.action import ExecutionType

PREV_ROOM = None

def go_bathroom(person):
    "Simulates a person going to the bathroom."
    global PREV_ROOM
    PREV_ROOM = person.current_room
    person.entered_building.enter_room(Bathroom, person)

def go_back(person):
    "Makes a person go back to the previous room."
    person.entered_building.enter_room(type(PREV_ROOM), person)

def __start_flush(person):
    person.current_room.find_sim_object(Toilet).activate()

def __stop_flush(person):
    person.current_room.find_sim_object(Toilet).deactivate()

def __use_toilet(person):
    person.toilet = 0

def use_toilet(person):
    "Simulates a person going to the toilet."
    person.act(go_bathroom)
    person.print_action("uses the toilet")
    person.act(__use_toilet, 1, 5)
    person.act(__start_flush)
    person.act(__stop_flush)
    person.act(go_back)

def __start_shower(person):
    person.current_room.find_sim_object(Shower).activate()

def __stop_shower(person):
    person.current_room.find_sim_object(Shower).deactivate()

def __use_shower(person):
    person.fun += 3
    person.tiredness -= 1
    # keep tiredness constant
    # shower can be either refreshing or relaxing

def use_shower(person):
    "Simulates a person using the shower."
    person.act(go_bathroom)
    person.print_action("uses the shower")
    person.act(__start_shower)
    person.act(__use_shower, 5, 20, exectype=ExecutionType.CONTINUOUS)
    person.act(__stop_shower)
    person.act(go_back)

def __start_bath(person):
    person.current_room.find_sim_object(Bath).activate()

def __stop_bath(person):
    person.current_room.find_sim_object(Bath).deactivate()

def __use_bath(person):
    person.fun += 2
    person.tiredness += 1

def use_bath(person):
    "Simulates a person taking a bath."
    person.act(go_bathroom)
    person.print_action("takes a bath")
    person.act(__start_bath)
    person.act(__use_bath, 25, 45, exectype=ExecutionType.CONTINUOUS)
    Alarm.set_after_minutes(person, __stop_bath, 20)
    person.act(go_back)
