
# 2020-11-06 08:00:03

from sys import stdout, path
path.append("..") # Adds higher directory to python modules path.

from tools import String_Builder

from core_AST import Val


# val implementation

class Int_Val(Val):
    # python operator overload
    # https://www.geeksforgeeks.org/operator-overloading-in-python/
    def __init__(self, value, value_type="INT"):
        # cast to Python integer type
        self.value = int(value)
        self.value_type = value_type

    def __add__(self, rhs):
        """return Int_Val class type. Type signature not hardcoded for future modification"""
        # assume rhs is also a Int_Val type
        result = Int_Val(self.value + rhs.value,  self.value_type)
        return result

    def __sub__(self, rhs):
        result = Int_Val(self.value - rhs.value,  self.value_type)
        return result

    def __mul__(self, rhs):
        result = Int_Val(self.value * rhs.value,  self.value_type)
        return result

    def __truediv__(self, rhs):
        # note that integer division will return integer
        result = Int_Val(self.value // rhs.value,  self.value_type)
        return result

    def __ge__(self, rhs):
        # greater or equal to
        result = None

        if self.value >= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __gt__(self, rhs):
        # greater or equal to
        result = None

        if self.value > rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result  

    def __le__(self, rhs):
        # greater or equal to
        result = None

        if self.value <= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result 
    
    def __lt__(self, rhs):
        # greater or equal to
        result = None

        if self.value < rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result 
    
    def __eq__(self, rhs):
        # this check is necessary because the program seems to pass None sometimes for rhs
        if rhs != None:

            # greater or equal to
            result = None

            if self.value == rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            result = Boolean_Val("false")
            
        return result 
    
    def __ne__(self, rhs):
        # this check is necessary because the program seems to pass None sometimes for rhs
        if rhs != None:

            # greater or equal to
            result = None

            if self.value != rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            result = Boolean_Val("false")
        
        return result

    # def typecheck(self, type_context):
        # pass

    # def eval(self, eval_context):
    #     pass

class Float_Val(Val):
    def __init__(self, value, value_type="FLOAT"):
        # cast to Python float type
        self.value = float(value)
        self.value_type = value_type

    def __add__(self, rhs):
        """return Float_Val class type. Type signature not hardcoded for future modification"""
        # assume rhs is also a Float_Val type
        result = Float_Val(self.value + rhs.value,  self.value_type)
        return result

    def __sub__(self, rhs):
        result = Float_Val(self.value - rhs.value,  self.value_type)
        return result

    def __mul__(self, rhs):
        result = Float_Val(self.value * rhs.value,  self.value_type)
        return result

    def __truediv__(self, rhs):
        # note that integer division will return integer
        result = Float_Val(self.value / rhs.value,  self.value_type)
        return result

    def __ge__(self, rhs):
        # greater or equal to
        result = None

        if self.value >= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __gt__(self, rhs):
        # greater or equal to
        result = None

        if self.value > rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result  

    def __le__(self, rhs):
        # greater or equal to
        result = None

        if self.value <= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result 
    
    def __lt__(self, rhs):
        # greater or equal to
        result = None

        if self.value < rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result 
    
    def __eq__(self, rhs):
        # this check is necessary because the program seems to pass None sometimes for rhs
        if rhs != None:

            # greater or equal to
            result = None

            if self.value == rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            result = Boolean_Val("false")
            
        return result 
    
    def __ne__(self, rhs):
        # this check is necessary because the program seems to pass None sometimes for rhs
        if rhs != None:

            # greater or equal to
            result = None

            if self.value != rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            result = Boolean_Val("false")
        
        return result
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
    def __init__(self, value, value_type="BOOLEAN"):
        self.value = value
        self.value_type = value_type

    # def typecheck(self, type_context):
    #     pass

    # def eval(self, eval_context):
    #     pass

    # def __str__(self):
        # """override parent class Val's method due to discrepancy"""