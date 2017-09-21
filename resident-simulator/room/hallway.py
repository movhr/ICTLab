"A hallway."
from room.roombase import Roombase
from assets.light import Light
from assets.heater import Heater

class Hallway(Roombase):
    "A hallway with one light and the heater installed in a separate compartment."
    def __init__(self):
        super(Hallway, self).__init__("hallway")
        self.add_object(Light, 3) #spread across the hallway
        self.add_object(Heater)
        Hallway.collect_usage_levels = self.collect_usage_levels_new

    def collect_usage_levels_new(self):
        "Overrides super function to add heater temperature"
        states = super(Hallway, self).collect_usage_levels()
        states.update({'temperature': self.find_sim_object(Heater).temperature})
        return states

    def update(self):
        self.find_sim_object(Heater).update()
        return super(Hallway, self).update()


