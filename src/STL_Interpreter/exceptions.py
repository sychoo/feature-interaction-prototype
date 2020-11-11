# Simon Chu
# 2020-11-07 14:31:49

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

import tools


class Error(RuntimeError):
    """super class that supports printing error message in bold red texts"""
    def __init__(self, msg):
        tools.Tools.print_error(msg)

class Context_Lookup_Error(Error):
    pass

class Type_Error(Error):
    pass

class Operator_Not_Found_Error(Error):
    pass

class Invalid_Signal_Error(Error):
    pass

class Parse_Error(Error):
    pass