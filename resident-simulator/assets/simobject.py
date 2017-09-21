"A module for generic simulator objects"


class SimObject(object):
    """An abstract class for defining objects that have an active state.
    Has an update method that must be overridden."""

    def __init__(self, power_usage=0, water_usage=0):
        self.name = ""
        self.is_active = False  # active state
        self.power_usage = power_usage  # Power _usage in Watts
        self.water_usage = water_usage  # Water _usage in Liters

    def update(self):
        "The function to run when active. Must be overridden."
        pass

    def set_id(self, id, roomname):
        self.name = roomname + '_' + type(self).__name__.lower() + '_' + id
        return self

    def activate(self):
        "Activates the simulated object."
        self.is_active = True
        print("activated %s." % self.name)

    def deactivate(self):
        "Deactivates the simulated object."
        self.is_active = False
        print("deactivated %s" % self.name)

    def collect_usage_levels(self):
        usage_levels = {"name": self.name}
        if self.water_usage > 0:
            usage_levels.update({'water': self.water_usage})
        if self.power_usage > 0:
            usage_levels.update({'power': self.power_usage})
        return usage_levels

    def collect_building_variables(self):
        """Must be passed as a variable.
        Returns all-time present variables in a building concerning this type."""
        pass
