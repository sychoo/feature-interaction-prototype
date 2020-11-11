# tools.py
# Mon 2020-11-02 13:42:26 EST

from termcolor import colored
from sys import stdout
from io import StringIO

import re # for string replacement

class Tools:
    @staticmethod
    def str_to_bool(string):
        if string == "true":
            return True
        elif string == "false":
            return False
        else:
            raise RuntimeError("string value \"" + string + "\" is not recognized and cannot be converted to boolean.")

    @staticmethod
    def bool_to_str(bool):
        if bool == True:
            return "true"
        elif bool == False:
            return "false"
        else:
            raise RuntimeError("boolean value \"" + bool + "\" is not recognized and cannot be converted to string.")

    @staticmethod
    def extract_raw_program_string(string):
        """extract raw program string from string, get rid of all single-line whitespaces
        handles preprocessing of the program
        """

        # initialize line list
        line_list = list()

        # specify regex for single-line comment and multi-line comments
        single_line_comment_pattern = r"\/\/(.*)"
        multi_line_comment_pattern = r"(\/\*(((.|\n)*)?)\*\/(\s)*)"

        # replace all single-line and multi-line comments
        string = re.sub(single_line_comment_pattern, "", string)
        string = re.sub(multi_line_comment_pattern, "", string)

        # get rid of all single line newline characters and single line whitespaces
        # split the program with delimiter \n
        splited_raw_program_string = string.split("\n")

        for line in splited_raw_program_string:

            # check whether the line only consist of whitespaces or a dangling newline character
            if not (line.isspace() or line == ""):
                line_list.append(line)
        
        # concatenate with (list of) lines with \n
        raw_program_string = "\n".join(line_list)

        # when the file is not empty, add \n at the end
        if len(raw_program_string) > 0:

            # add \n at the end if there isn't any
            if raw_program_string[-1] != "\n":
                raw_program_string += "\n"
                
        return raw_program_string

    # original 
    # @staticmethod
    # def extract_raw_program_string(string):
    #     """extract raw program string from string, get rid of all single-line whitespaces"""
    #     # initialize line list
    #     line_list = list()

    #     # split the program with delimiter \n
    #     splited_raw_program_string = string.split("\n")

    #     for line in splited_raw_program_string:

    #         # check whether the line only consist of whitespaces
    #         if not (line.isspace() or line == ""):
    #             line_list.append(line)
        
    #     # concatenate with (list of) lines with \n
    #     raw_program_string = "\n".join(line_list)

    #     # add \n at the end if there isn't any
    #     if raw_program_string[-1] != "\n":
    #         raw_program_string += "\n"
            
    #     return raw_program_string


    @staticmethod
    def get_raw_program_string(program_file):
        """get the raw program string based on the program_file given. It will get rid of all single line \n's in the program"""
        string = ""

        # read the entire file as a string
        with open(program_file, "r") as program_file_line_stream:
            string = program_file_line_stream.read()

        return Tools.extract_raw_program_string(string)

    # original
    # @staticmethod
    # def get_raw_program_string(program_file):
    #     """get the raw program string based on the program_file given. It will get rid of all single line \n's in the program"""
    #     # initialize line list
    #     line_list = list()

    #     # open the program file with read permission, get the line stream
    #     with open(program_file, "r") as program_file_line_stream:
    #         for line in program_file_line_stream:

    #             # check whether the line only consist of whitespaces
    #             if not (line.isspace()):
    #                 line_list.append(line)

    #     # print(line_list) #debug

    #     # concatenate the (list of) lines of the program
    #     raw_program_string = "".join(line_list)

    #     return raw_program_string

    
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
        """check suffix of file name supplied. return boolean value that represent whether the file name conform with the suffix
        set default suffix to .stl
        """

        is_correct_suffix = program_file_name.endswith(suffix)
        if is_correct_suffix:
            return
        else:
            Tools.print_warning("Invalid file name. File must end with .stl\n")
            exit(0)

    @staticmethod
    def check_token_length(token_stream):# # find the number of tokens
        # find number of tokens
        token_num = Tools.token_length(token_stream)

        if token_num <= 0:
            exit(0)

    @staticmethod
    def token_length(token_stream):
        """find the number of tokens"""
        token_num = 0
        for _ in token_stream:
            token_num += 1
        
        return token_num

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