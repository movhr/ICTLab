"Simulates a toilet."

from assets.simobject import SimObject

class Toilet(SimObject):
    "Simulates a toilet."
    def __init__(self):
        super(Toilet, self).__init__(water_usage=6)

    def update(self):
        return
