# tools.py
# Mon 2020-11-02 13:42:26 EST

from termcolor import colored
from sys import stdout
from io import StringIO

class Tools:
    @staticmethod
    def get_raw_program_string(program_file):
        """get the raw program string based on the program_file given. It will get rid of all single line \n's in the program"""
        # initialize line list
        line_list = list()

        # open the program file with read permission, get the line stream
        with open(program_file, "r") as program_file_line_stream:
            for line in program_file_line_stream:
                if line != "\n":
                    line_list.append(line)

        # concatenate the (list of) lines of the program
        raw_program_string = "".join(line_list)

        return raw_program_string

    
    @staticmethod
    def print_error(error_msg):
        """print error message, this will prepend Error: to the string given in bolded red"""
        stdout.write(colored("Error: " + error_msg, "red", attrs=["bold"]))

    @staticmethod
    def print_warning(warning_msg):
        """print warning message, this will print the given string in bolded yellow"""
        stdout.write(colored(warning_msg, "yellow", attrs=["bold"]))

    @staticmethod
    def check_suffix(program_file_name, suffix=".stl"):
        """check suffix of file name supplied. return boolean value that represent whether the file name conform with the suffix"""
        is_correct_suffix = program_file_name.endswith(suffix)
        if is_correct_suffix:
            return
        else:
            Tools.print_warning("Invalid file name. File must end with .stl\n")
            exit(0)

# https://stackoverflow.com/questions/2414667/python-string-class-like-stringbuilder-in-c
class String_Builder:
    """accumulate string more efficiently"""
    string = None

    def __init__(self):
        self.string = StringIO()

    def append(self, str):
        self.string.write(str)

    def __str__(self):
        return self.string.getvalue()