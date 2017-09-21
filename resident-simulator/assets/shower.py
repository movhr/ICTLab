"Simulates a shower."

from assets.simobject import SimObject

class Shower(SimObject):
    "Simulates a shower."
    def __init__(self):
        #power _usage is average 1.5kW/10 min for electric shower
        super(Shower, self).__init__(power_usage=150, water_usage=8)

    def update(self):
        return
