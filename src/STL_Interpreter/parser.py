# Mon 2020-11-02 14:53:40 EST

# Simon Chu
# 2019-10-06 21:38:06 Sun EDT
# Program to define the parser

from rply import ParserGenerator
import ast

from lexer import Lexer
from sys import argv
from tools import Tools
import os

class Eval_Context:
    @staticmethod
    def get_empty_context():
        return Eval_Context()

class Type_Context:
    @staticmethod
    def get_empty_context():
        return Type_Context()

class Parser:
    """
    Hierachy:
        stmt_list : statement list
        stmt : statement
        expr : expression
        val : value

    """
    def __init__(self):
        # define the reserved words for the parser
        # A list of all token names, accepted by the parser.
        pg = ParserGenerator([

            # logical operators
            "LOGICAL_AND", 
            "LOGICAL_OR",
            "LOGICAL_IMPLIES",

            # binary operators for numerical (Int, Float) operations
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "GREATER",
            "LESS",

            # binary logical operators for both numerical (Int, Float) and Boolean operations
            "EQUAL_EQUAL",
            "NOT_EQUAL",

            # program control structure
            # "WHILE",
            # "FOR",
            # "IF",
            # "ELSE",

            # print/display operator
            "PRINTLN",
            "PRINT",

            # content grouping structures
            "L_PAREN",
            "R_PAREN",
            "L_BRACE",
            "R_BRACE",
            "L_SQ_BRACE",
            "R_SQ_BRACE",

            # primary arithmetic operators
            "EQUAL",
            "PLUS",
            "MINUS",
            "MULTIPLY",
            "DIVIDE",

            # separators/delimiters
            "COMMA",
            "SEMICOLON",
            "NEWLINE",

            # numerical values
            "FLOAT",
            "INT",
            "STRING",
            "BOOLEAN",

            # declarations
            "VAL_DECL",
            "VAR_DECL",

            # LTL/STL unary operators
            "GLOBALLY",
            "EVENTUALLY",
            "NEXT",

            # LTL/STL binary operators
            "UNTIL",
            "RELEASE",

            # identifiers (variable identifiers/type identifiers)
            "IDENTIFIER",
            ],

            # ["PLUS", "MINUS", "MULTIPLY", "DIVIDE", "SEMICOLON",
            #  "PRINT", "PRINTLN", "STRING", "EQUAL", "IDENTIFIER", "BOOLEAN",
            #  "LBRACE", "RBRACE", "LPAREN", "RPAREN", "IF", "ELSE", "BOOLEAN_AND",
            #  "BOOLEAN_OR", "EQUAL_EQUAL", "NOT_EQUAL", "GREATER", "LESS", "GREATER_EQUAL",
            #  "LESS_EQUAL", "WHILE", "FOR"
            #  ],

            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['LPAREN', 'RPAREN']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV']),
                ('right', ['EQUAL']),
            ])

        # parser definition

        # top-level statements
        @pg.production("main : stmt_list")
        def main(s):
            """parse top level statements, encapsulate entire program structure"""

            # return the statement block
            return s[0]


        @pg.production("stmt_list : stmt_list stmt")
        def multi_line_stmt(s):
            """parse multi-line statements"""

            # append the statement to the statements list
            return ast.Stmt_List(s[0].get_stmt_list() + [s[1]])


        @pg.production("stmt_list : stmt")
        def single_line_stmt(s):
            """parse single-line statements"""
            return ast.Stmt_List([s[0]])


        @pg.production("stmt : L_BRACE stmt_list R_BRACE")
        def stmt_list_block(s):
            """parse block of statement list"""
            return ast.Stmt_List(s[1])

        # combine two similar statements
        @pg.production("stmt : PRINT expr separator")
        @pg.production("stmt : PRINTLN expr separator")
        def print_stmt(s):
            """parse print/println statements"""
            return ast.Print_Stmt(s[1], s[0].gettokentype())


        @pg.production("stmt : expr separator")
        def single_expr_stmt(s):
            return s[0]


        @pg.production("expr : val")
        def single_val_expr(s):
            """parse single value expression, simply return the """
            return s[0]


        @pg.production("val : INT")
        def int_val(s):
            """parse Int values"""
            return ast.Int_Val(s[0].getstr(), s[0].gettokentype())


        @pg.production("val : FLOAT")
        def float_val(s):
            """parse Float values"""
            return ast.Float_Val(s[0].getstr(), s[0].gettokentype())


        @pg.production("val : STRING")
        def string_val(s):
            """parse Float values"""
            return ast.String_Val(s[0].getstr(), s[0].gettokentype())

        @pg.production("val : BOOLEAN")
        def boolean_val(s):
            """parse Float values"""
            return ast.Boolean_Val(s[0].getstr(), s[0].gettokentype())

        @pg.production("separator : SEMICOLON")
        @pg.production("separator : NEWLINE")
        @pg.production("separator : SEMICOLON NEWLINE")
        def separator(s):
            """parse separators
            separator can be one of the following:
                - ;
                - \n
                - ;\n
            """
            pass

        # build the parser
        self.parser = pg.build()

    # return the parsedAST
    def parse(self, token_stream):
        return self.parser.parse(token_stream)

def main():
    """check right amount of the command line arguments and start the lexcial analyzer"""

    if len(argv) == 2:
        # 2 command line arguments (sys.argv[1]: program file)
        # interpret the program file supplied by user

        # check whether the file exists in the file system
        if os.path.exists(argv[1]):

            # check suffix of the file
            Tools.check_suffix(argv[1])

            # create lexer
            lexer = Lexer()

            # lexical analyze the program given, break it down to token stream
            token_stream = lexer.lex(Tools.get_raw_program_string(argv[1]))

            # create parser
            parser = Parser()

            # parse the lexical token stream to AST (abstract syntax tree)
            parsed_ast = parser.parse(token_stream)

            print(parsed_ast)

        else:
            Tools.print_error("file \"" + argv[1] + "\" does not exists in the file system.\n")   
    else:
        # other number of command line arguments
        # print usage message
        Tools.print_warning("Usage: python main.py <program-to-run>\n")


if __name__ == "__main__":
    main()