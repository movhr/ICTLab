"Module for actions and execution types."

from enum import Enum

class ExecutionType(Enum):
    "Offers different kinds of execution types."
    AFTER_EXECUTIONTIME = 0 #use execution time as blocking mechanism
    BEFORE_EXECUTIONTIME = 1 #use execution time as cooldown
    CONTINUOUS = 2

class Action(object):
    "Represents an action which a person can execute."
    def __init__(self, action, executiontime, executiontype):
        self.execute = action
        self.exec_time = executiontime
        self.exec_type = executiontype
        self.is_active = False
