# core_AST.py
# 2020-11-06 07:43:58
# Simon Chu

# for implementing abstract method
import abc

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder
import exceptions

class Eval_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the value associated with it

    Attributes:
        context: {"var_id": evaluated_var_value, ...}
        use id string for the key of the dictionary to boost the look up speed and efficiency
    """

    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_expr, var_value, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()"""
        var_id = id_expr.get_id()

        # update the current context
        self.context.update({var_id: {"var_value": var_value, "attr": attr}})

        # if identifier (key) is defined in the outer context, also
        # update the binding for the outer context

        # if this is not on the top-level
        if self.outer_context != None:
            if (var_id in self.get_outer_context_var_id()):
                self.outer_context.update({var_id: {"var_value": var_value, "attr": attr}})


    def lookup(self, id_expr):
        try:
            return self.context[id_expr.get_id()]["var_value"]
        except KeyError:
            raise exceptions.Context_Lookup_Error(
                "Identifier \"" + id_expr.get_id() + "\" specified is not in the scope of the evaluation context.")

    def __str__(self):
        return str(self.context)
    
    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Eval_Context()

    def get_current_context_var_id(self):
        # get a list of variable identifier (in string) in the current context
        return self.context.keys()

    def get_outer_context_var_id(self):
        if self.outer_context != None:
            # get a list of variable identifier (in string) in the outer context
            return self.outer_context.keys()

class Type_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the type associated with it

    Attributes:
        context: {"var_id": evaluated_var_type, ...}
    """
    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_expr, var_type, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()
        attr: attributes of the id_expr (by declaration)
        """
        var_id = id_expr.get_id()

        # update the current context
        self.context.update({var_id: {"var_type": var_type, "attr": attr}})

        # if identifier (key) is defined in the outer context, also
        # update the binding for the outer context

        # if this is not on the top-level
        if self.outer_context != None:
            if (var_id in self.get_outer_context_var_id()):
                self.outer_context.update({var_id: {"var_type": var_type, "attr": attr}})

    def lookup(self, id_expr):
        try:
            return self.context[id_expr.get_id()]["var_type"]
        except KeyError:
            raise exceptions.Context_Lookup_Error(
                "Identifier \"" + id_expr.get_id() + "\" specified is not in the scope of the type context.")

    def __str__(self):
        return str(self.context)
    
    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Eval_Context()

    def get_current_context_var_id(self):
        # get a list of variable identifier (in string) in the current context
        return self.context.keys()

    def get_outer_context_var_id(self):
        if self.outer_context != None:
            # get a list of variable identifier (in string) in the outer context
            return self.outer_context.keys()


class Node(metaclass=abc.ABCMeta):
    """root super class for all nodes in the AST (abstract syntax tree)"""

    def isSubTypeOf(self, other):
        return type(self) is type(other)
        
    # # equal operator overload
    # def __eq__(self, other):
    #     if not isinstance(other, Node):
    #         return NotImplemented
    #         # __dict__ contains object's symbol table
    #     return (type(self) is type(other) and self.__dict__ == other.__dict__)

    
    # # not equal to operator overload

    # def __ne__(self, other):
    #     return not (self == other)

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

class Id_Expr(Expr):
    """stores identifier of the variable, variable expression
    stores 
            type signature
            variable identifier signature
            and STL formula operator
    """

    def __init__(self, var_id):
        """take the identifier name of the variable"""
        self.var_id = var_id

    def __str__(self):
        sb = String_Builder()
        sb.append("Var_Expr: ( ")
        sb.append(self.var_id)
        sb.append(" )")

        return str(sb)

    def get_id(self):
        return self.var_id

    def eval(self, eval_context):
        return eval_context.lookup(self)

    
    def typecheck(self):
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

class STL_Expr(Expr):

    def typecheck(self, type_context):
        pass

    def eval(self, eval_context):
        pass

    def __str__(self):
        pass