"Module for simulating a home cinema system"

from assets.simobject import SimObject

class Tv(SimObject):
    "Simulates a TV."
    def __init__(self, power_usage=111):
        super(Tv, self).__init__(power_usage)

    def update(self):
        return
