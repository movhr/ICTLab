"Module for simulating a light"

from assets.simobject import SimObject

class Light(SimObject):
    "Defines a light"
    def __init__(self, power_usage=9):
        super(Light, self).__init__(power_usage)

    def update(self):
        return
