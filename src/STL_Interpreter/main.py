# main.py
#
# main interpreter file
#
# support both REPL (read-eval-print loop) and program file input
# depending on whether command line argument is given

# Sun Nov  1 16:56:03 EST 2020
# Designed with ❤️ by Simon Chu

# for color print
# Documentation: https://pypi.org/project/termcolor/
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
# termcolor.COLORS gives you a list of colours
from termcolor import colored

# import the tools
from tools import Tools

# for command line arguments
from sys import stdout, argv
import io
import sys
from contextlib import redirect_stdout

# for file existence checking
import os

# for gracefully terminate when Control-C happens
from signal import signal, SIGINT

from lexer import Lexer
from parser import Parser
import AST

INTERPRETER_VERSION = "1.0.0"

class Interpreter:
    """supports interpreting the program, or entering REPL (read-eval-print loop)
    
    Standard in the Interpreter class
        output is printed using stdout.write(), or sys.stdout.write() (instead of print())
        warning messages is printed using Interpret.print_warning()
        error message is printed using Interpret.print_error()

    Usage:
        REPL (read-eval-print loop) Mode:
            Ctrl-C: clean line, it will abort the current line user is writing,
                    and go to the next line
            Ctrl-D: exit program. This will exit REPL mode and abort the current REPL process.

        Program Input Mode:
            python3 main.py <program-to-run>

    Attributes:
        program_file: a string that stores the program to be interpreted
    """

    def __init__(self, program_file=None):
        """interpret the program file given"""
        # accept the parameters if it is given
        if program_file != None:
            self.program_file = program_file
            raw_program_string = Tools.get_raw_program_string(self.program_file)
            self.interpret(raw_program_string)

        # otherwise, create an empty object with no parameters, enter REPL loop
        else:
            self.repl_list = list()
            self.repl()


    @staticmethod
    def input_arrow():
        return colored(">>> ", "green", attrs=["bold"])


    def repl(self):
        """enter REPL (read-eval-print loop)"""

        # print header information
        stdout.write("STL Interpreter " + INTERPRETER_VERSION + "\n")
        stdout.write("Designed with ❤️  by Simon Chu\n")
        stdout.write("Copyright © 2020 Carnegie Mellon University. All rights reserved.\n")

        # handle the case when user clicks Ctrl-C or SIGINT
        def handler(signal_received, frame):
            stdout.write("\nKeyboardInterrupt")
            stdout.write("\n" + self.input_arrow())

        while True:
            # Tell Python to run the handler() function when SIGINT is recieved
            signal(SIGINT, handler)

            # add the 3 green arrows in the REPL
            stdout.write(self.input_arrow())

            # obtain user input
            try:
                input_line = input() # user input will be printed using system color
                
                # TO-DO: run the line through lexer and parser to ensure correctness, then append to the repl_list
                # MAYBE: support muli-line expressions like Python

                if Interpreter.repl_interpret(self.repl_list, input_line):
                    # case when interpreter exit with no error, append expression to repl_list
                    self.repl_list.append(input_line + '\n')

                # get the raw program string from the list
                # raw_program_string = "".join(self.repl_list)

                # interpret the program with the added line
                # TO-DO: make sure only display the stdout for the last executed command
                # self.interpret(raw_program_string)

            except EOFError: 
                # catch Ctrl-D input
                stdout.write("\nEOF\n")
                exit(0)

            except Exception as e:
                # trap all other errors (without exiting REPL)
                print(e)

    @staticmethod
    def repl_interpret(prev_repl_list, input_line):
        """start the REPL interpretation of the program
        
        The way repl_interpret is implemented is as follows
        1. evaluate the expression prior to the current input line (accumulated throughout the prior REPL session)
        2. evaluate the new line input by the user

        3. redirect/omit the standard output of the evaluation of the previous session program
        4. only display the standard output of the evaluation of the new line
        """

        # extract raw program strings for the previous repl list and the new input line
        prev_raw_program_string = Tools.extract_raw_program_string("".join(prev_repl_list))
        new_raw_program_string = Tools.extract_raw_program_string(input_line)



        # Evaluation for the prevous REPL List
        # create the Lexer
        lexer = Lexer()
        prev_token_stream = lexer.lex(prev_raw_program_string)

        # replica of token stream for checking the length
        # since token stream can only be looped once, we have to replicate it
        prev_token_stream_replica = lexer.lex(prev_raw_program_string)

        # create type and evaluation contexts
        prev_type_context = AST.Type_Context.get_empty_context()
        prev_eval_context = AST.Eval_Context.get_empty_context()

        # find the length of the token stream, return if token is empty (no user input)
        if Tools.token_length(prev_token_stream_replica) != 0:
            # create parser
            parser = Parser()
            prev_parsed_AST = parser.parse(prev_token_stream)

            # start the type checking process
            prev_parsed_AST.typecheck(prev_type_context)

            # debug
            # redirect the output to somewhere else
            # sys.stdout = open(os.devnull, "w")

            # start the evaluation process
            prev_parsed_AST.eval(prev_eval_context)

            # recover the stdout stream
            # sys.stdout = sys.__stdout__

        # Evaluation for the new line
        # create the Lexer
        lexer = Lexer()
        new_token_stream = lexer.lex(new_raw_program_string)

        # replica of token stream for checking the length
        # since token stream can only be looped once, we have to replicate it
        new_token_stream_replica = lexer.lex(new_raw_program_string)

        # create type and evaluation contexts (reuse the one created for the previous REPL list)
        new_type_context = prev_type_context
        new_eval_context = prev_eval_context

        # find the length of the token stream, return if token is empty (no user input)
        if Tools.token_length(new_token_stream_replica) != 0:
            # create parser
            parser = Parser()

            try:
                new_parsed_AST = parser.parse(new_token_stream)

                # start the type checking process
                new_parsed_AST.typecheck(new_type_context)

                Tools.print_warning("OUTPUT >>>\n")

                # start the evaluation process
                new_parsed_AST.eval(new_eval_context)

                Tools.print_warning("<<< OUTPUT\n")

                # append the line to the repl_list
                return True

                
            except Exception as e:
                print(e)
                return False

        return False

    @staticmethod
    def interpret(raw_program_string):
        """start the interpretation of the program"""

        # create the Lexer
        lexer = Lexer()
        token_stream = lexer.lex(raw_program_string)

        # replica of token stream for checking the length
        # since token stream can only be looped once, we have to replicate it
        token_stream_replica = lexer.lex(raw_program_string)

        # find the length of the token stream
        Tools.check_token_length(token_stream_replica)
        
        # create parser
        parser = Parser()
        parsed_AST = parser.parse(token_stream)

        # start the type checking process
        parsed_AST.typecheck(AST.Type_Context.get_empty_context())

        # start the evaluation process
        parsed_AST.eval(AST.Eval_Context.get_empty_context())


def main():
    """main function that get called when executing the Python program"""
    if len(argv) == 1:
        # 1 command line argument (no additional arguments)
        # enter REPL loop 
        Interpreter()

    elif len(argv) == 2:
        # 2 command line arguments (sys.argv[1]: program file)
        # interpret the program file supplied by user

        # check suffix of the file
        Tools.check_suffix(argv[1])

        # check whether the file exists in the file system
        if os.path.exists(argv[1]):
            Interpreter(argv[1])

        else:
            Tools.print_error("file \"" + argv[1] + "\" does not exists in the file system.\n")   
    else:
        # other number of command line arguments
        # print usage message
        Tools.print_warning("Usage: python main.py <program-to-run>\n")


if __name__ == "__main__":
    main()
