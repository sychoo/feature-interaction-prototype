# stmt.py
# 2020-11-06 07:48:34
# contains core statement of the language

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import Stmt

# stmt implementation
class Val_Decl_Stmt(Stmt):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass


class Var_Decl_Stmt(Stmt):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass


class Assign_Stmt(Stmt):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass


class Print_Stmt(Stmt):
    """stores either print or println expression"""

    def __init__(self, expr, token_type):
        self.expr = expr
        self.token_type = token_type

    def typecheck(self, type_context):
        self.expr.typecheck(type_context)

    def eval(self, eval_context):
        # evaluate the embedded expression in the print statement (if it is not None)
        # only PRINTLN is allowed None -> to print an empty line
        if self.expr != None:
            self.expr = self.expr.eval(eval_context)

            if self.token_type == "PRINT":
                stdout.write(self.expr.to_str())

            elif self.token_type == "PRINTLN":
                stdout.write(self.expr.to_str())
                stdout.write("\n")

        else:
            if self.token_type == "PRINTLN":
                stdout.write("\n")

    def __str__(self):
        sb = String_Builder()
        sb.append("Print_Stmt: ( ")
        sb.append(str(self.expr))
        sb.append(", ")
        sb.append(str(self.token_type))
        sb.append(" )")

        return str(sb)

# /stmt implementation