# Mon 2020-11-02 14:53:40 EST

# Simon Chu
# 2019-10-06 21:38:06 Sun EDT
# Program to define the parser

from rply import ParserGenerator
import AST

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
            # parse signals
            "SIGNAL",

            # logical operators
            "LOGICAL_AND", 
            "LOGICAL_OR",
            "LOGICAL_IMPLIES",
            "LOGICAL_NOT",

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
            "COLON",

            # numerical values
            "FLOAT",
            "INT",
            "STRING",
            "BOOLEAN",

            # declarations
            "VAL_DECL",
            "VAR_DECL",

            # # LTL/STL unary operators
            # "GLOBALLY",
            # "EVENTUALLY",
            # "NEXT",

            # # LTL/STL binary operators
            # "UNTIL",
            # "RELEASE",

            # identifiers (variable identifiers/type identifiers)
            "IDENTIFIER",
            ],


            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            # the top has the highest precedence
            # https://www.mathcs.emory.edu/~valerie/courses/fall10/155/resources/op_precedence.html
            precedence=[
                ('left', ['LPAREN', 'RPAREN']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MULTIPLY', 'DIVIDE']),
                ('left', ['GREATER_EQUAL', 'LESS_EQUAL', 'GREATER', 'LESS', 'EQUAL_EQUAL', 'NOT_EQUAL']),
                ('left', ['LOGICAL_NOT']),
                ('left', ['LOGICAL_AND']),
                ('left', ['LOGICAL_OR']),
                ('right', ['EQUAL']),
                ('nonassoc', ['PRINT', 'PRINTLN']) # non-associative
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
            return AST.Stmt_List(s[0].get_stmt_list() + [s[1]])


        @pg.production("stmt_list : stmt")
        def single_line_stmt(s):
            """parse single-line statements"""
            return AST.Stmt_List([s[0]])


        # # block statements
        # @pg.production("stmt : L_BRACE stmt_list r_brace_as_separator")
        # def stmt_list_block(s):
        #     """parse block of statement list"""
        #     return AST.Stmt_List(s[1])


        # typed val declaration (type inference)
        @pg.production("stmt : VAL_DECL expr EQUAL expr separator")
        def untyped_var_decl_stmt(s):
            return AST.Val_Decl_Stmt(s[0].gettokentype(), s[1], None, s[3])

    
        # untyped var declaration (type inference)
        @pg.production("stmt : VAR_DECL expr EQUAL expr separator")
        def untyped_var_decl_stmt(s):
            return AST.Var_Decl_Stmt(s[0].gettokentype(), s[1], None, s[3])

        

        # typed val declaration
        @pg.production("stmt : VAL_DECL expr COLON expr EQUAL expr separator")
        def typed_val_decl_stmt(s):
            return AST.Val_Decl_Stmt(s[0].gettokentype(), s[1], s[3], s[5])


        # typed var declaration
        @pg.production("stmt : VAR_DECL expr COLON expr EQUAL expr separator")
        def typed_val_decl_stmt(s):
            return AST.Var_Decl_Stmt(s[0].gettokentype(), s[1], s[3], s[5])

        # assignment statement (non-declaration style)
        @pg.production("stmt : expr EQUAL expr separator")
        def assign_stmt(s):
            return AST.Assign_Stmt(s[0], s[2])


        # combine two similar statements
        @pg.production("stmt : PRINT expr separator")
        @pg.production("stmt : PRINTLN expr separator")
        def print_stmt(s):
            """parse print/println statements"""
            return AST.Print_Stmt(s[1], s[0].gettokentype())

        @pg.production("stmt : PRINTLN separator")
        def single_println_stmt(s):
            return AST.Print_Stmt(None, s[0].gettokentype())

        @pg.production("stmt : expr separator")
        def single_expr_stmt(s):
            return s[0]

        @pg.production("expr : IDENTIFIER")
        def var_expr(s):
            return AST.Id_Expr(s[0].getstr())

        @pg.production("expr : L_PAREN expr R_PAREN")
        def parent_expr(s):
            """calculate the parenthesized expression first"""
            return s[1]

        @pg.production("expr : expr GREATER expr")
        @pg.production("expr : expr GREATER_EQUAL expr")
        @pg.production("expr : expr LESS expr")
        @pg.production("expr : expr LESS_EQUAL expr")
        @pg.production("expr : expr EQUAL_EQUAL expr")
        @pg.production("expr : expr NOT_EQUAL expr")
        def binary_comp_expr(s):
            """handles binary comparison expressions"""
            return AST.Binary_Comp_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])

        @pg.production("expr : LOGICAL_NOT expr")
        def unary_logic_expr(s):
            pass

        @pg.production("expr : expr LOGICAL_AND expr")
        @pg.production("expr : expr LOGICAL_OR expr")
        @pg.production("expr : expr LOGICAL_IMPLIES expr")
        def binary_logic_expr(s):
            """handles binary logic expressions"""
            return AST.Binary_Logic_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])

        @pg.production("expr : expr PLUS expr")
        @pg.production("expr : expr MINUS expr")
        @pg.production("expr : expr DIVIDE expr")
        @pg.production("expr : expr MULTIPLY expr")
        def binary_arith_expr(s):
            """handles binary logic expressions"""
            return AST.Binary_Arith_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])


        # G[1, 10](condition)(t, <signal>)
        @pg.production("expr : IDENTIFIER L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN L_PAREN expr COMMA val R_PAREN")        
        def unary_STL_expr_1(s):
            """handles unary STL expressions (G: Globally, F: Eventually)"""
            # obtain the operator of the STL expression

            op = s[0].getstr()
            if op == "G":
                return AST.G_STL_Expr(op, s[2], s[4], s[7], s[10], s[12])
            elif op == "F":
                return AST.F_STL_Expr(op, s[2], s[4], s[7], s[10], s[12])
            else:
                raise RuntimeError("STL Operator: " + op + " not recognized.")

            # X need to be handled separately

        @pg.production("expr : IDENTIFIER L_SQ_BRACE expr R_SQ_BRACE L_PAREN expr R_PAREN L_PAREN expr COMMA val R_PAREN") 
        def unary_STL_expr_2(s):
            """handle unary STL expressions (X: next)"""
            op = s[0].getstr()
            if op == "X":
                return AST.X_STL_Expr(op, s[2], s[5], s[8], s[10])

        @pg.production("expr : L_PAREN expr R_PAREN IDENTIFIER L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN L_PAREN expr COMMA val R_PAREN")
        def binary_STL_expr(s):
            """handler binary STL expressions"""
            return AST.Binary_STL_Expr(s[3].getstr(), s[5], s[7], s[1], s[10], s[13], s[15])


        @pg.production("expr : val")
        def single_val_expr(s):
            """parse single value expression, simply return the """
            return s[0]


        @pg.production("val : INT")
        def int_val(s):
            """parse Int values"""
            return AST.Int_Val(s[0].getstr(), s[0].gettokentype())


        @pg.production("val : FLOAT")
        def float_val(s):
            """parse Float values"""
            return AST.Float_Val(s[0].getstr(), s[0].gettokentype())


        @pg.production("val : STRING")
        def string_val(s):
            """parse Float values"""
            return AST.String_Val(s[0].getstr(), s[0].gettokentype())


        @pg.production("val : BOOLEAN")
        def boolean_val(s):
            """parse Float values"""
            return AST.Boolean_Val(s[0].getstr(), s[0].gettokentype())

        @pg.production("val : SIGNAL")
        def boolean_val(s):
            """parse Float values"""
            return AST.Signal_Val(s[0].getstr(), s[0].gettokentype())

        # @pg.production("r_brace_as_separator : R_BRACE")
        # @pg.production("r_brace_as_separator : R_BRACE separator")
        # def r_brace_as_separator(s):
        #     """helper function for block statement { stmt_list }
        #     R_BRACE itself can act as a separator
        #     """
        #     pass

        @pg.production("separator : NEWLINE")
        @pg.production("separator : SEMICOLON")
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

            # get the raw program string
            raw_program_string = Tools.get_raw_program_string(argv[1])

            # lexical analyze the program given, break it down to token stream
            token_stream = lexer.lex(raw_program_string)

            # replica of token stream for checking the length
            # since token stream can only be looped once, we have to replicate it
            token_stream_replica = lexer.lex(raw_program_string)

            # find the length of the token stream
            Tools.check_token_length(token_stream_replica)
            
            # create parser
            parser = Parser()

            # parse the lexical token stream to AST (abstract syntax tree)
            parsed_AST = parser.parse(token_stream)

            print(parsed_AST)

        else:
            Tools.print_error("file \"" + argv[1] + "\" does not exists in the file system.\n")   
    else:
        # other number of command line arguments
        # print usage message
        Tools.print_warning("Usage: python main.py <program-to-run>\n")


if __name__ == "__main__":
    main()
