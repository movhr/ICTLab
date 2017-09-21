"A bathroom."
from room.roombase import Roombase
from assets.toilet import Toilet
from assets.shower import Shower
from assets.bath import Bath
from assets.light import Light

class Bathroom(Roombase):
    "A bathroom containing a toilet, shower and bath."
    def __init__(self):
        super(Bathroom, self).__init__("bathroom")
        self.add_object(Toilet)
        self.add_object(Shower)
        self.add_object(Bath)
        self.add_object(Light, 4) #spot lights
