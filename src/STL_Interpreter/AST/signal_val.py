
from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import Val

class Signal_Val(Val):
    def __init__(self, value, value_type):
        # in the future, parse the value directory to JSON object in Python
        self.value = value
        self.value_type = value_type
