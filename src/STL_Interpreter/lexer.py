# Sun Nov  1 18:32:24 EST 2020
# lexer.py
#
# lexer definition file
#
# support both REPL (read-eval-print loop) and program file input
# depending on whether command line argument is given

# Sun Nov  1 16:56:03 EST 2020
# Designed with ❤️ by Simon Chu

# https://rply.readthedocs.io/en/latest/
from rply import LexerGenerator
from sys import argv
from tools import Tools
import os

class Lexer:
    def __init__(self):
        """Initialize Lexical Analyzer
        To test the Lexer class, execute
            python3 lexer.py <program-to-run>

        Attributes:
            lexer: the lexer that is built
        
        \s can be one of the following
        _ : space
        \t: tab
        \r: carriage return
        \n: new line
        \v: vertical tab
        """

        # initialize the lexer generator
        lg = LexerGenerator()

        # ignore all whitespaces except newline
        lg.ignore(r"(\t|\ |\v|\r)+")

        # ignore all single-line comments and all white spaces afterwards

        # original
        # lg.ignore(r"\/\/(.*)?\n") 
        # lg.ignore(r"\/\/(.*)") # match up to but not including the \n character

        # lg.ignore(r"\/\/(.|\n)*") 

        # ignore all multi-line comments and white spaces afterwards
        # references
        # https://stackoverflow.com/questions/13014947/regex-to-match-a-c-style-multiline-comment
        # https://regex101.com
        # note that ? is lazy (match as few character as possible)
        # note that . matches all characters except line terminators
        # original
        # lg.ignore(r"(\/\*(((.|\n)*)?)\*\/(\s)*)")  

        
        # lg.ignore(r"\s+") # ignore all white spaces



        # lg.ignore(r"^\n$") # ignore all except new line

        # signal representation
        # https://stackoverflow.com/questions/32155133/regex-to-match-a-json-string
        # Note that everything is atomic, JSON does not need backtracking if it's valid
        # and this prevents catastrophic backtracking
#         lg.add("SIGNAL", r"(?(DEFINE)\
# (?<json>(?>\s*(?&object)\s*|\s*(?&array)\s*))\
# (?<object>(?>\{\s*(?>(?&pair)(?>\s*,\s*(?&pair))*)?\s*\}))\
# (?<pair>(?>(?&STRING)\s*:\s*(?&value)))\
# (?<array>(?>\[\s*(?>(?&value)(?>\s*,\s*(?&value))*)?\s*\]))\
# (?<value>(?>true|false|null|(?&STRING)|(?&NUMBER)|(?&object)|(?&array)))\
# (?<STRING>(?>\"(?>\\(?>[\"\\\/bfnrt]|u[a-fA-F0-9]{4})|[^\"\\\0-\x1F\x7F]+)*\"))\
# (?<NUMBER>(?>-?(?>0|[1-9][0-9]*)(?>\.[0-9]+)?(?>[eE][+-]?[0-9]+)?))\
# )\
# \A(?&json)\z\
# ")

        # lg.add("SIGNAL", r"\{.*\:\{.*\:.*\}\}")
        # https://stackoverflow.com/questions/2583472/regex-to-validate-json
        # lg.add("SIGNAL", r"[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]")


        lg.add("SIGNAL", r"\$\{(.|\n)*?\}\$")

        # logical operators
        lg.add("LOGICAL_AND", r"\&\&")
        lg.add("LOGICAL_OR", r"\|\|")
        lg.add("LOGICAL_IMPLIES", r"\=\>")

        # binary operators for numerical (Int, Float) operations
        lg.add("GREATER_EQUAL", r"\>\=")
        lg.add("LESS_EQUAL", r"\<\=")
        lg.add("GREATER", r"\>")
        lg.add("LESS", r"\<")

        # binary logical operators for both numerical (Int, Float) and Boolean operations
        lg.add("EQUAL_EQUAL", r"\=\=")
        lg.add("NOT_EQUAL", r"\!\=")

        lg.add("LOGICAL_NOT", r"\!")

        # program control structure
        # lg.add("WHILE", r"while")
        # lg.add("FOR", r"for")
        # lg.add("IF", r"if")
        # lg.add("ELSE", r"else")

        # print/display operator
        lg.add("PRINTLN", r"println")
        lg.add("PRINT", r"print")

        # content grouping structures
        lg.add("L_PAREN", r"\(")
        lg.add("R_PAREN", r"\)")
        lg.add("L_BRACE", r"\{")
        lg.add("R_BRACE", r"\}")
        lg.add("L_SQ_BRACE", r"\[")
        lg.add("R_SQ_BRACE", r"\]")

        # primary arithmetic operators
        lg.add("EQUAL", r"\=")
        lg.add("PLUS", r"\+")
        lg.add("MINUS", r"-")
        lg.add("MULTIPLY", r"\*")
        lg.add("DIVIDE", r"/")

        # separators/delimiters
        lg.add("COMMA", r",")
        lg.add("SEMICOLON", r";")
        lg.add("COLON", r":")
        lg.add("NEWLINE", r"\n")
        
        # numerical values
        # current use . as a identifier for floating-point numbers
        # in the future, maybe find ways to include 158E2 as floating points
        # lg.add("FLOAT", r"[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?") # XX.XX
        # lg.add("FLOAT", r"[0-9]*((\.[0-9]+)|(\.?[0-9]+([eE][-+]?[0-9]+)))")

        # support 1.2, 1E7, 1.E7, 1.02E2 (equivalent to 102.0) as floating-point numbers
        lg.add("FLOAT", r"[0-9]*(\.[0-9]+([eE][-+]?[0-9]+)?)|([0-9]+([eE][-+]?[0-9]+))")
        lg.add("INT", r"\d+")
        lg.add("STRING", r"\".*\"")
        lg.add("BOOLEAN", r"true|false")

        # declarations
        lg.add("VAL_DECL", r"val")
        lg.add("VAR_DECL", r"var")

        # # LTL/STL unary operators
        # lg.add("GLOBALLY", r"\$G")
        # lg.add("EVENTUALLY", r"\$F")
        # lg.add("NEXT", r"\$X")

        # # LTL/STL binary operators
        # lg.add("UNTIL", r"\$U")
        # lg.add("RELEASE", r"\$R")

        # identifiers (variable identifiers/type identifiers/STL operator identifier)
        lg.add("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*")

        lg.add("META_IDENTIFIER", r"\$[a-zA-Z_][a-zA-Z0-9_.]*")
        
        # build the lexer
        self.lexer = lg.build()

    # parse raw program string to token stream
    def lex(self, raw_program_string):
        return self.lexer.lex(raw_program_string)


def main():
    """check right amount of the command line arguments and start the lexcial analyzer"""

    if len(argv) == 2:
        # 2 command line arguments (sys.argv[1]: program file)
        # interpret the program file supplied by user

        # check suffix of the file
        Tools.check_suffix(argv[1])

        # check whether the file exists in the file system
        if os.path.exists(argv[1]):

            # create lexer
            lexer = Lexer()

            # get the raw program string
            raw_program_string = Tools.get_raw_program_string(argv[1])
            
            # lexical analyze the program given, break it down to token stream
            token_stream = lexer.lex(raw_program_string)

            # print all tokens identified
            for token in token_stream:
                print(token)

        else:
            Tools.print_error("file \"" + argv[1] + "\" does not exists in the file system.\n")   
    else:
        # other number of command line arguments
        # print usage message
        Tools.print_warning("Usage: python main.py <program-to-run>\n")


if __name__ == "__main__":
    main()
