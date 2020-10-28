# STL.py
# file to parse and eval STL formulas

# Wed Oct 21 20:32:53 EDT 2020
# Designed with ❤️ by Simon Chu

import abc
from algorithms import Algorithms

class STL_Error(RuntimeError):
    pass

class STL_Expr(metaclass=abc.ABCMeta):
    """support the evaluation of STL formulas
    """
    @abc.abstractmethod
    def eval(self, signal):
        """abstract method to eval the STL formula with respect to the signal"""
        pass


class Global(STL_Expr):
    """support global expression G"""
    def __init__(self, begin, end, stl_expr):
        self.begin = begin
        self.end = end
        self.stl_expr = stl_expr
        # self.external_data = external_data

    def eval(self, signal, external_data=dict()):
        # pass
        # assume G include both bound
        for time in range(self.begin, self.end + 1):
            # evaluate all signal data between the time interval

            # echo all truth values
            # print(self.stl_expr.eval(signal.get_signal_data_by_time(time), external_data))
            result = self.stl_expr.eval(signal.get_signal_data_by_time(time), external_data)

            # debug
            # print(result)
            if result == False:
                return False
        return True
            

class Helper():
    # assume the evaluation of ego drone
    class Distance_To_Boundary(STL_Expr):
        def __init__(self):
            pass
    
        def eval(self, signal_element, external_data):
            """return the min distance to boundary"""
            ego_coord = signal_element.get_signal_data_by_id_key("Ego", "current_coord")
            return Algorithms.min_distance_to_boundary(ego_coord, external_data["internal_map"])

    class Distance_To_Enemy_Drone(STL_Expr):
        def __init__(self):
            pass

        def eval(self, signal_element, external_data):
            ego_coord = signal_element.get_signal_data_by_id_key("Ego", "current_coord")
            enemy_coord = signal_element.get_signal_data_by_id_key("Enemy", "current_coord")
            return Algorithms.distance_between_2_points(ego_coord, enemy_coord)


class Primitives():
    """support primitive expressions"""
    class Greater_Than(STL_Expr):
        def __init__(self, lhs_stl_expr, rhs_stl_expr):
            self.lhs_stl_expr = lhs_stl_expr
            self.rhs_stl_expr = rhs_stl_expr

        def eval(self, signal_data, external_data):
            lhs = None
            rhs = None

            # debug
            # print(type(self.lhs_stl_expr), type(self.rhs_stl_expr))

            # evaluate lhs
            if isinstance(self.lhs_stl_expr, int) or isinstance(self.lhs_stl_expr, float):
                lhs = self.lhs_stl_expr
            else:
                lhs = self.lhs_stl_expr.eval(signal_data, external_data)
            
            # evaluate rhs
            if isinstance(self.rhs_stl_expr, int) or isinstance(self.rhs_stl_expr, float):
                rhs = self.rhs_stl_expr
            else:
                rhs = self.rhs_stl_expr.eval(signal_data, external_data)
            
            # debug
            # print(type(lhs), type(rhs))

            # both side must be integers before proceeding
            if (isinstance(lhs, int) or isinstance(lhs, float)) and (isinstance(rhs, int) or isinstance(rhs, float)):
                return lhs > rhs
            else:
                raise STL_Error("one or both STL expressions cannot be evaluated to integer")

    class Less_Than(STL_Expr):
        def __init__(self, lhs_stl_expr, rhs_stl_expr):
            self.lhs_stl_expr = lhs_stl_expr
            self.rhs_stl_expr = rhs_stl_expr

        def eval(self, signal_data, external_data):
            lhs = None
            rhs = None

            # debug
            # print(type(self.lhs_stl_expr), type(self.rhs_stl_expr))

            # evaluate lhs
            if isinstance(self.lhs_stl_expr, int) or isinstance(self.lhs_stl_expr, float):
                lhs = self.lhs_stl_expr
            else:
                lhs = self.lhs_stl_expr.eval(signal_data, external_data)
            
            # evaluate rhs
            if isinstance(self.rhs_stl_expr, int) or isinstance(self.rhs_stl_expr, float):
                rhs = self.rhs_stl_expr
            else:
                rhs = self.rhs_stl_expr.eval(signal_data, external_data)
            
            # debug
            # print(type(lhs), type(rhs))

            # both side must be integers before proceeding
            if (isinstance(lhs, int) or isinstance(lhs, float)) and (isinstance(rhs, int) or isinstance(rhs, float)):
                return lhs < rhs
            else:
                raise STL_Error("one or both STL expressions cannot be evaluated to integer")
