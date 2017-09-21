"A kitchen."
from room.roombase import Roombase
from assets.light import Light
from assets.stove import Stove
from assets.microwave import  Microwave

class Kitchen(Roombase):
    "A kitchen containing 6 lights, a stove and a microwave."
    def __init__(self):
        super(Kitchen, self).__init__("kitchen")
        self.add_object(Light, 2) #Hanging lights
        self.add_object(Light, 3) #Built in lights
        self.add_object(Stove) #Stove for cooking
        self.add_object(Microwave) #For warming up food
        #TODO: add fridge
