# Mon 2020-11-02 14:55:14

# for implementing abstract method
import abc

from tools import String_Builder


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
        pass

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

    def __init__(self, expr, token_type):
        self.expr = expr
        self.token_type = token_type

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        sb = String_Builder()
        sb.append("Print_Stmt: ( ")
        sb.append(str(self.expr))
        sb.append(", ")
        sb.append(str(self.token_type))
        sb.append(" )")

        return str(sb)

# /stmt implementation



# expr implementation

class STL_Expr(Expr):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass

# /expr implementation



# val implementation

class Int_Val(Val):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass


class Float_Val(Val):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass


class String_Val(Val):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass


class Boolean_Val(Val):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    # def __str__(self):
        # """override parent class Val's method due to discrepancy"""
        

# /val implementation