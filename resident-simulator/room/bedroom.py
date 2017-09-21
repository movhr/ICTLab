"A bedroom."
from room.roombase import Roombase
from assets.light import Light
from assets.tv import Tv

class Bedroom(Roombase):
    "A bedroom containing a nightstand, hanging lamp and TV."
    def __init__(self):
        super(Bedroom, self).__init__("bedroom")
        self.add_object(Light, 4) #hanging lamp
        self.add_object(Light) #nightstand
        self.add_object(Tv)
