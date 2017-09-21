"Module for simulating a central heating system"

from assets.simobject import SimObject

class Heater(SimObject):
    "Defines the central heating system"
    def __init__(self, power_usage=2200):
        super(Heater, self).__init__(power_usage)
        self.wamingSpeed = 0.1 #warms up 0.1C per minute
        self.temperature = 18 #starting room temperature
        self.desiredTemperature = 20
        self.standardTemperature = 16

    def update(self):
        if self.is_active:
            if self.desiredTemperature > self.temperature:
                self.temperature += self.wamingSpeed
                #print("Heater is running (room temp: %i)." % self.temperature)
        else:
            if self.temperature > self.standardTemperature:
                self.temperature -= self.wamingSpeed
                #print("Heater is turned off (room temp: %i)." % self.temperature)
        return (self.power_usage, self.water_usage)

    def SetDesiredTemperature(self, temp):
        self.desiredTemperature = temp

    def collect_building_variables(self):
        return [{'temperature': self.temperature}]
