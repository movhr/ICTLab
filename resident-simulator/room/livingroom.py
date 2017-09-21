"A living room."
from room.roombase import Roombase
from assets.light import Light
from assets.tv import Tv

class LivingRoom(Roombase):
    "A living room containing a TV and multiple lights."
    def __init__(self):
        super(LivingRoom, self).__init__("living_room")
        self.add_object(Tv)
        self.add_object(Light, 2) #standalone lights
        self.add_object(Light, 2) #hanging lamp dining part
        self.add_object(Light, 2) #hanging lamp relaxing part
        