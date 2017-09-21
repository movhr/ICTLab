"Simulates a bath object."

from assets.simobject import SimObject

class Bath(SimObject):
    "A simulated bath object."
    def __init__(self):
        # bath uses 160 liters avg
        # bath is always running for 20 minutes
        # water _usage = 160/20=8
        super(Bath, self).__init__(power_usage=150, water_usage=8)

    def update(self):
        return
