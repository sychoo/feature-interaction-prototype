# stmt.py
# 2020-11-06 07:48:34
# contains core statement of the language

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import Stmt

class Variable_Decl_Stmt(Stmt):
    def __init__(self, decl_type, var_id_val, var_type, rhs_expr):
        self.decl_type = decl_type
        self.var_id_val = var_id_val
        self.var_type = var_type
        self.rhs_expr = rhs_expr

    def __str__(self):
        sb = String_Builder()
        sb.append("Variable_Decl_Stmt: ( ")
        sb.append(str(self.decl_type))
        sb.append(" ")
        sb.append(str(self.var_id_val))
        sb.append(": ")
        sb.append(str(self.var_type))
        sb.append(" = ")
        sb.append(str(self.rhs_expr))
        sb.append(" )")
        return str(sb)

# stmt implementation
class Val_Decl_Stmt(Variable_Decl_Stmt):
    # do not allow re-assignment for val declaration

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        # add val_decl attribute
        self.rhs_expr = self.rhs_expr.eval(eval_context)
        eval_context.add(self.var_id_val, self.rhs_expr)



class Var_Decl_Stmt(Variable_Decl_Stmt):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        # add var_decl attribute
        self.rhs_expr = self.rhs_expr.eval(eval_context)
        eval_context.add(self.var_id_val, self.rhs_expr)



class Assign_Stmt(Stmt):

    def __init__(self, var_id_val, rhs_expr):
        self.var_id_expr = var_id_val
        self.rhs_expr = rhs_expr

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        # test whether if the lhs id_expr is assignable (using the context) before the assignment
        # val cannot be reassigned

        self.rhs_expr = self.rhs_expr.eval(eval_context)
        eval_context.add(self.var_id_expr, self.rhs_expr)

    def __str__(self):
        sb = String_Builder()
        sb.append("Assign_Stmt: ( ")
        sb.append(str(self.var_id_expr))
        sb.append(" = ")
        sb.append(str(self.rhs_expr))
        sb.append(" )")

        return str(sb)


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
                # print(type(self.expr))
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