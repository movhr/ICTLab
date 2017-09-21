"Building simulator module"

from assets.heater import Heater
from room.bedroom import Bedroom
from room.livingroom import LivingRoom
from room.kitchen import Kitchen
from room.hallway import Hallway
from room.bathroom import Bathroom


class Building(object):

    def __init__(self, name, world):
        self.name = name
        self.world = world

        self.power_usage = 0
        self.water_usage = 0
        self.kwh = 0  # kiloWatt-hour of power _usage
        self.cm = 0  # cubic meters of water _usage

        self.rooms = []
        self.rooms.append(Hallway())
        self.rooms.append(LivingRoom())
        self.rooms.append(Bedroom())
        self.rooms.append(Kitchen())
        self.rooms.append(Bathroom())
        self.heater = next(room for room in self.rooms if isinstance(
            room, Hallway)).find_sim_object(Heater)

        self.variables = [self.heater.collect_building_variables, self.get_time_building_variable]

    def update(self):
        "Must be called every minute. Collects the usage levels of all the rooms' active objects."
        for room in self.rooms:
            pu, wu = room.update()
            self.power_usage += pu
            self.water_usage += wu

    def collect_usage_levels(self):
        result = []
        for room in self.rooms:
            states = room.collect_usage_levels()
            if len(states['assets']) == 0:
                continue
            result.append({
                'room_name': type(room).__name__,
                "assets": states['assets']
            })
        return result

    def collect_building_variables(self):
        variables = {}
        for variable in self.variables:
            for vdict in variable():
                variables.update(vdict)
        return variables

    def update_usage_levels(self):
        "Must be called hourly to aggregate usage levels."
        # Collect power levels
        added_kwh = float(self.power_usage) / 60000
        self.kwh += added_kwh
        print ("Used %3f kWh this  hour (total: %3f kWh)." %
               (added_kwh, self.kwh))
        self.power_usage = 0

        # Collect water levels
        added_cm = float(self.water_usage) / 1000
        self.cm += added_cm
        print("Used %3f m3 water this hour (total: %3f m3)." %
              (added_cm, self.cm))
        self.water_usage = 0

        return

    def leave_room(self, person):
        if person.current_room is not None:
            print("%s left the %s" %
                  (person.name, type(person.current_room).__name__))
            person.current_room.turn_off_lights()
            person.current_room = None

    def enter_room(self, roomclass, person):
        for room in self.rooms:
            if isinstance(room, roomclass):
                self.leave_room(person)
                print("%s entered the %s" % (person.name, roomclass.__name__))
                person.current_room = room
                return room.turn_on_lights()
        raise RuntimeError

    def turn_on_heater(self):
        self.heater.activate()

    def turn_off_heater(self):
        self.heater.deactivate()

    def get_time_building_variable(self):
        return [{'clock': self.world.GetDateTime().strftime('%s')}]