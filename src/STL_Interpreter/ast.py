# Mon 2020-11-02 14:55:14

# for implementing abstract method
import abc

from tools import String_Builder
from sys import stdout

class Eval_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the value associated with it
    """

    @staticmethod
    def get_empty_context():
        return Eval_Context()


class Type_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the type associated with it
    """

    @staticmethod
    def get_empty_context():
        return Type_Context()


class Node(metaclass=abc.ABCMeta):
    """root super class for all nodes in the AST (abstract syntax tree)"""

    def isSubTypeOf(self, other):
        return type(self) is type(other)
        
    # equal operator overload
    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
            # __dict__ contains object's symbol table
        return (type(self) is type(other) and self.__dict__ == other.__dict__)

    
    # not equal to operator overload

    def __ne__(self, other):
        return not (self == other)

    def type(self):
        return type(self)

    @abc.abstractmethod
    def eval(self, eval_context):
        pass

    @abc.abstractmethod
    def typecheck(self, type_context):
        pass

    @abc.abstractmethod
    def __str__(self):
        """method to display the string representation of the AST for parser"""
        pass

# 3 primitive structures

# - Statement list : Stmt_List (Block)

# - Statement : Stmt
# - Expression (things that gets evaluated to a value (no side effects)) : Expr
# - Value : primitive values

# top-level classes

class Stmt_List(Node):
    """store a list of statements
    Attributes:
        statements: list of statements
    """
    def __init__(self, stmts):
        self.stmts = stmts

    def get_stmt_list(self):
        return self.stmts

    def interpret(self, ctx):
        for stmt in self.stmts:
            stmt.interpret(ctx)

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):

        # evaluate all statements in the statement list
        for stmt in self.stmts:
            stmt.eval(eval_context)

    def __str__(self):
        sb = String_Builder()

        for stmt in self.stmts:
            sb.append(str(stmt) + "\n")

        return str(sb)
            
class Stmt(Node):
    """super class for statements"""
    pass

class Expr(Stmt):
    """super class for expressions"""
    pass

class Val(Expr):
    """super class for values, store primitive value types"""
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type # note that type is a reserved word

    def __str__(self):
        sb = String_Builder()
        sb.append("Val: ( ")
        sb.append(str(self.value))
        sb.append(", ")
        sb.append(str(self.value_type))
        sb.append(" )")
        return str(sb)
    
    def to_str(self):
        return str(self.value)

    def eval(self, eval_context):
        return self

    def typecheck(self, type_context):
        return self.value_type
# /top-level classes


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
        if self.expr != None:
            expr_val = self.expr.eval(eval_context)

            if self.token_type == "PRINT":
                stdout.write(expr_val.to_str())

            elif self.token_type == "PRINTLN":
                stdout.write(expr_val.to_str())
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

class Binary_Expr(Expr):
    """super class for binary expressions"""
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        

# expr implementation
class Binary_Comp_Expr(Binary_Expr):
    """stores binary comparison operation expression AST, except Binary STL expressions"""
    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass

class Binary_Logic_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass

class STL_Expr(Expr):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass

class Unary_STL_Expr(STL_Expr):
    def __init__(self, op, begin_expr, end_expr, condition_expr):
        self.op = op
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        self.condition_expr = condition_expr

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
        sb.append(") )")

        return str(sb)


# /expr implementation

class Binary_STL_Expr(STL_Expr):
    def __init__(self, op, begin_expr, end_expr, begin_condition_expr, end_condition_expr):
        self.op = op
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        self.begin_condition_expr = begin_condition_expr
        self.end_condition_expr = end_condition_expr

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
        sb.append(") )")

        return str(sb)

# val implementation

class Int_Val(Val):
    pass
    # def typecheck(self, type_context):
        # pass

    # def eval(self, eval_context):
    #     pass


class Float_Val(Val):
    pass
    # def typecheck(self, type_context):
    #     pass

    # def eval(self, eval_context):
    #     pass


class String_Val(Val):
    def to_str(self):
        """override to_str method in Val class
        get rid of the double quotes for the string
        """
        return self.value[1:-1]
    # def typecheck(self, type_context):
    #     pass

    # def eval(self, eval_context):
    #     pass


class Boolean_Val(Val):
    pass
    # def typecheck(self, type_context):
    #     pass

    # def eval(self, eval_context):
    #     pass

    # def __str__(self):
        # """override parent class Val's method due to discrepancy"""
        

# /val implementation