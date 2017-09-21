"Simulates a person in a designated world."

from random import Random
from person.action import Action, ExecutionType
from person.routine import Routine
from person.eating import eat
from person.working import work
from person.sleeping import sleep
from person.sanitary import use_toilet
from room.hallway import Hallway
from room.bedroom import Bedroom

class Person(object):
    "A simulated person in a designated world"
    def __init__(self, name, home, world):
        self.name = name
        self.hunger = 500
        self.tiredness = 0
        self.toilet = 0
        self.fun = 50
        self.world = world
        self.home = home
        self.entered_building = home
        self.current_room = next(room for room in home.rooms if isinstance(room, Bedroom))
        self.action_queue = []
        self.routine = Routine(self)
        self.is_sleeping = True


    def update(self):
        "Updates a person's levels."
        if self.is_sleeping:
            self.hunger += 0.5
            self.toilet += 0.5
        else:
            self.hunger += 1
            self.tiredness += 1
            self.toilet += 1
            self.fun -= 1
        self.think()

    def print_action(self, msg):
        "Prints a message with a time prefix and person's name."
        print("%s %s %s." % (self.world.datetime.strftime("[%a %d-%m-%Y %H:%M:%S]"), self.name, msg))

    def enter_building(self, building):
        "Makes a person enter a building."
        self.entered_building = building
        self.entered_building.turn_on_heater()
        self.print_action("entered building " + building.name)
        self.entered_building.enter_room(Hallway, self)

    def leave_building(self):
        "Makes a person leave a building."
        self.entered_building.leave_room(self)
        self.entered_building.turn_off_heater()
        self.print_action("left building " + self.entered_building.name)
        self.entered_building = None

    def sitrep(self):
        "Prints a person's levels."
        print("Sitrep of %s." % self.name)
        self.print_action("'s fun level is " + str(self.fun))
        self.print_action("'s hunger level is " + str(self.hunger))
        self.print_action("'s sleep level is " + str(self.tiredness))
        self.print_action("'s bathroom level is " + str(self.toilet))

    def act(self, func, mintime=0, maxtime=0, exectype=ExecutionType.AFTER_EXECUTIONTIME):
        "Adds an action to the person's action queue."
        action = Action(func, mintime if maxtime == 0 else Random().randint(mintime, maxtime), exectype)
        self.action_queue.append(action)
        return action

    def think(self):
        "Activates the next action in the person's action queue."
        if self.entered_building is None:
            #self.print_action("is not home.")
            return

        # First update the action queue, and if any actions must be performed,
        # perform when person is done doing their thing
        if len(self.action_queue) > 0:
            current_action = self.action_queue[0]
            # If action is present but not active, activate it
            if not current_action.is_active:
                current_action.is_active = True
                # Instant action
                if current_action.exec_time == 0:
                    current_action.execute(self)
                    self.print_action("does " + current_action.execute.__name__)
                    self.action_queue.pop(0)
                else:
                    # Action with preparation/cooldown
                    # If action must be executed before cooldown, act it
                    # Or if continuously, begin doing it
                    if current_action.exec_type == ExecutionType.BEFORE_EXECUTIONTIME or current_action.exec_type == ExecutionType.CONTINUOUS:
                        current_action.execute(self)
                    self.print_action("starts doing " + current_action.execute.__name__)
                    current_action.exec_time -= 1
                return
            # Action is active and time reaches 0
            # execute it if it's a prep action
            elif current_action.exec_time == 0:
                if current_action.exec_type == ExecutionType.AFTER_EXECUTIONTIME:
                    current_action.execute(self)
                self.print_action("finishes " + current_action.execute.__name__)
                self.action_queue.pop(0)
                return
            # Action is still pending
            elif current_action.exec_time > 0:
                # If action is continuous, repeat
                if current_action.exec_type == ExecutionType.CONTINUOUS:
                    current_action.execute(self)
                current_action.exec_time -= 1
                self.print_action("is doing " + current_action.execute.__name__)
                return

        # If the person is sleeping, they cant act anything
        if self.is_sleeping:
            self.print_action("is sleeping...")
            return

        # Check on person's levels to act upon
        self.print_action("is thinking")

        # First check on their daily routine
        # self.routine.update(self.world.GetTime())

        # every 2-3 hours person must use the toilet
        # eating increases toilet, thus set limit little further
        if self.toilet > 200:
            return use_toilet(self)

        # every 13-15 hours is bedtime, depending on person's sleep quality
        # TODO: let tiredness depend on activities (hobbies/work)
        if self.tiredness > 900 or self.world.IsNowBetween(23, 0, 0, 0):
            self.print_action("'s sleep level is " + str(self.tiredness))
            return sleep(self)

        #every 5 hours, the person is really hungry
        #every 2 hours, the person can use a snack,
        if self.hunger > 120:
            self.print_action("'s hunger level is " + str(self.hunger))
            return eat(self)

        # Check on person's daily activities
        if self.world.IsNowBetween(8, 30, 9, 0) and self.world.IsTodayWeekday():
            work(self)
            return
