# Simon Chu
# 2020-11-07 14:31:49

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

import tools

class Error(RuntimeError):
    def __init__(self, msg):
        tools.Tools.print_error(msg)

class Context_Lookup_Error(Error):
    pass