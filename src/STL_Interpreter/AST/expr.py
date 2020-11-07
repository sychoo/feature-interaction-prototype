# 2020-11-06 07:53:43
from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import Expr


class Binary_Expr(Expr):
    """super class for binary expressions"""
    def __init__(self, op_str, op_type, lhs_expr, rhs_expr):
        self.op_str = op_str
        self.op_type = op_type
        self.lhs_expr = lhs_expr
        self.rhs_expr = rhs_expr
        
    def __str__(self):
        sb = String_Builder()
        sb.append("Binary_Expr: ( ")
        sb.append(str(self.lhs_expr))
        sb.append(" ")
        sb.append(str(self.op_str))
        sb.append(" ")
        sb.append(str(self.rhs_expr))
        sb.append(" ) ")
        return str(sb)

# expr implementation
class Binary_Comp_Expr(Binary_Expr):
    """stores binary comparison operation expression AST, except Binary STL expressions"""
    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.lhs_expr = self.lhs_expr.eval(eval_context)
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        result = None

        if self.op_type == "GREATER":
            result = self.lhs_expr > self.rhs_expr
        elif self.op_type == "GREATER_EQUAL":
            result = self.lhs_expr >= self.rhs_expr
        elif self.op_type == "LESS":
            result = self.lhs_expr < self.rhs_expr
        elif self.op_type == "LESS_EQUAL":
            result = self.lhs_expr <= self.rhs_expr
        elif self.op_type == "EQUAL_EQUAL":
            result = self.lhs_expr == self.rhs_expr
        elif self.op_type == "NOT_EQUAL":
            result = self.lhs_expr != self.rhs_expr
        else:
            raise RuntimeError("Operator \""  + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Binary_Logic_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        """support short-circuit evaluation? sure but under the premise that the type is the same"""
        pass

    def __str__(self):
        pass

class Binary_Arith_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.lhs_expr = self.lhs_expr.eval(eval_context)
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        result = None

        if self.op_type == "PLUS":
            result = self.lhs_expr + self.rhs_expr
        elif self.op_type == "MINUS":
            result = self.lhs_expr - self.rhs_expr
        elif self.op_type == "MULTIPLY":
            result = self.lhs_expr * self.rhs_expr
        elif self.op_type == "DIVIDE":
            result = self.lhs_expr / self.rhs_expr
        else:
            raise RuntimeError("Operator \""  + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")
        
        return result

