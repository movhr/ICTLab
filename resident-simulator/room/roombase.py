from assets.light import Light
import sys #debug

class Roombase(object):
    "A base class for a room."

    def __init__(self, name):
        self.objects = []
        self.name = name

    def add_object(self, objclass, n=1):
        "Adds a specific amount of objects (default 1). obj: A SimObject class"
        nItems = 0
        for i in range(len(self.objects)):
            if type(self.objects[i]).__name__ == objclass.__name__:
                nItems += 1
        for i in range(n):
            newObj = objclass()
            newObj.set_id(str((nItems + i)), self.name)
            self.objects.append(newObj)
        return self

    def update(self):
        "Collects the power and water usage for active objects."
        pu = 0
        wu = 0
        for obj in self.objects:
            if obj.is_active:
                pu += obj.power_usage
                wu += obj.water_usage
        return pu, wu

    def find_sim_objects(self, objclass):
        "Finds all the objects that are an instance of a specific class in the room."
        for obj in self.objects:
            if isinstance(obj, objclass):
                yield obj

    def find_sim_object(self, objclass):
        "Finds the first object of a specific class in the room."
        for obj in self.objects:
            if isinstance(obj, objclass):
                return obj
        raise Exception

    def turn_on_lights(self, n=0):
        "Turns on a specific amount of lights."
        i = 0
        for obj in self.find_sim_objects(Light):
            obj.activate()
            i += 1
            if n > 0 and i == n:
                return self
        return self

    def turn_off_lights(self, n=0):
        "Turns off a specific amount of lights."
        i = 0
        for obj in self.find_sim_objects(Light):
            obj.deactivate()
            i += 1
            if n > 0 and i == n:
                return self
        return self

    def keep_on_lights(self, n):
        "Turns off a specific amount of lights until n remain on."
        i = 0
        for obj in self.find_sim_objects(Light):
            if i < n:
                i += 1
                continue
            elif i == n:
                return self
            else:
                obj.deactivate()
        return self

    def collect_usage_levels(self):
        "Collects the water and power usage of all active objects in the room."
        states = {'assets': []}
        i = 0
        for asset in self.objects:
            if asset.is_active:
                states['assets'].append(asset.collect_usage_levels())
                i += 1
        return states
