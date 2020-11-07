# 2020-11-06 07:57:20

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import STL_Expr



class Unary_STL_Expr(STL_Expr):
    def __init__(self, op, begin_expr, end_expr, condition_expr, time, signal):
        self.op = op
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        self.condition_expr = condition_expr
        self.time = time
        self.signal = signal

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_STL_Expr: ( ")
        sb.append(self.op)
        sb.append(" [")
        sb.append(str(self.begin_expr))
        sb.append(", ")
        sb.append(str(self.end_expr))
        sb.append("] (")
        sb.append(str(self.condition_expr))
        sb.append(") (")
        sb.append(str(self.time))
        sb.append(", ")
        sb.append(str(self.signal))
        sb.append(") )")

        return str(sb)


# /expr implementation

class Binary_STL_Expr(STL_Expr):
    def __init__(self, op, begin_expr, end_expr, begin_condition_expr, end_condition_expr, time_expr, signal_val):
        self.op = op
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        self.begin_condition_expr = begin_condition_expr
        self.end_condition_expr = end_condition_expr
        self.time_expr = time_expr
        self.signal_val = signal_val

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        sb = String_Builder()
        sb.append("Binary_STL_Expr: ( ")
        sb.append("(")
        sb.append(str(self.begin_condition_expr))
        sb.append(") ")
        sb.append(self.op)
        sb.append(" [")
        sb.append(str(self.begin_expr))
        sb.append(", ")
        sb.append(str(self.end_expr))
        sb.append("] (")
        sb.append(str(self.end_condition_expr))
        sb.append(") (")
        sb.append(str(self.time))
        sb.append(", ")
        sb.append(str(self.signal))
        sb.append(") )")

        return str(sb)

class G_STL_Expr(Unary_STL_Expr):
    """support the globally STL expression"""
    pass


class F_STL_Expr(Unary_STL_Expr):
    """support the future STL expression"""
    pass

class X_STL_Expr(Unary_STL_Expr):
    """support the future STL expression"""
    # override Unary_STL_Expr init function
    def __init__(self, op, time_interval_expr, condition_expr, time_expr, signal_val):
        self.op = op
        self.time_interval_expr = time_interval_expr
        self.condition_expr = condition_expr
        self.time_expr = time_expr
        self.signal_val = signal_val

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_STL_Expr: ( ")
        sb.append(self.op)
        sb.append(" [")
        sb.append(str(self.time_interval_expr))
        sb.append("] (")
        sb.append(str(self.condition_expr))
        sb.append(") (")
        sb.append(str(self.time_expr))
        sb.append(", ")
        sb.append(str(self.signal_val))
        sb.append(") )")

        return str(sb)