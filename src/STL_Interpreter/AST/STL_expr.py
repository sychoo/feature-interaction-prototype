# 2020-11-06 07:57:20

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import STL_Expr
from val import Meta_Id_Val



class Unary_STL_Expr(STL_Expr):
    def __init__(self, op, begin_expr, end_expr, condition_expr, time_expr, signal_val):
        self.op = op
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        self.condition_expr = condition_expr
        self.time_expr = time_expr
        self.signal_val = signal_val

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
        sb.append(str(self.time_expr))
        sb.append(", ")
        sb.append(str(self.signal_val))
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
        sb.append(str(self.time_expr))
        sb.append(", ")
        sb.append(str(self.signal_val))
        sb.append(") )")

        return str(sb)

class G_STL_Expr(Unary_STL_Expr):
    """support the globally STL expression"""
    def eval(self, eval_context):
        """add the pointer to the signal val to the context "$this$ -> signal_dict"""

        # debug
        # print(eval_context)

        #op, begin_expr, end_expr, condition_expr, time, signal):
        # evaluate the begin and the end time and time (time start for the signal)
        self.begin_expr = self.begin_expr.eval(eval_context)
        self.end_expr = self.end_expr.eval(eval_context)
        self.time_expr = self.time_expr.eval(eval_context)
        self.signal_val = self.signal_val.eval(eval_context)

        # convert both time to Python Int object
        self.begin_expr_int = self.begin_expr.to_py_obj()
        self.end_expr_int = self.end_expr.to_py_obj()
        self.time_expr_int = self.time_expr.to_py_obj()

        # only keep the signal value between certain time interval
        # $this -> slided Signal val
        # add $this meta variable to the context that refer to the signal that is currently begin evaluated
        eval_context.add(Meta_Id_Val("$this"), self.signal_val.slice_signal_by_time_interval(self.begin_expr_int, self.end_expr_int))

        # print(eval_context)
        # for time in range(self.begin_expr_int + self.time_expr_int, self.end_expr_int + 1 + self.time_expr_int):
            # eval_context.add(Meta_Id_Val("$" + str(time) + ".content"), self.signal_val.get_signal_dict()[str(time)])

        # TODO: add values in the signal (self.signal) to the evaluation_context
        # loop through time_begin to time_end (int)
        
        # add to_py_obj(self) to primitive values and signal value (dictionary)
        # i.e. [2, 3] evaluate $2.param and $3.param
        
        # $1.param -> 7
        # $2.param -> 10
        # $3.param -> 15
        # Lexer: META_IDENTIFIER = $ IDENTIFIER
        # META_IDENTIFIER.eval(context, signal)
        # eval function will evaluate all META_IDENTIFIERS associated with the param
        
        # implicitly evaluate the meta variables
        self.condition_expr = self.condition_expr.eval(eval_context)

        return self.condition_expr





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