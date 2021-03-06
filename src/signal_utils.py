# signal_utils.py
# program to support the evaluation of STL on signals generated by the drones

# Wed Oct 21 12:21:20 EDT 2020
# Designed with ❤️ by Simon Chu

# code to support the signal estimation
# using the algorithm embedded in the drone class
# also depends on what kind of mission ego drone is operating upon
# - fixed mission
# - wait point
# - free style

# Note the signal is relatively independent from most of the system
# it cannot contain any of the system objects (except coords object)
# everything that it contains has to be alpha numeric for readability
# and reasonability

from drone_utils import Shared_Flight_Data, ATC_Flight_Data

class Signal_Estimator:
    # estimate based on current fixed mission and the current signal
    def __init__(self, current_signal_element, drone_list=list()):
        self.drones = drone_list
        self.current_signal = current_signal_element

        # calculate current x and y based on current signal, and set it to the corresponding drone
        for drone in drone_list:
            # current_x_cor = current_signal_element.get_signal_data_by_id_key(drone.identifier, "current_coord").x()
            # current_y_cor = current_signal_element.get_signal_data_by_id_key(drone.identifier, "current_coord").y()
            current_coord = current_signal_element.get_signal_data_by_id_key(drone.identifier, "current_coord")
            drone.set_current_coord(current_coord)
            # drone.set_current_location(current_x_cor, current_y_cor)

    def add_drone(self, new_drone):
        self.drones.append(new_drone)

    # sample response_data:
    # {'Ego': {'current_x_cor': 11, 'current_y_cor': 8, 'current_map_cell': (11, 8) : 1}, 'Enemy': {'current_x_cor': 11, 'current_y_cor': 9, 'current_map_cell': (11, 9) : 1}, 'step': 9}
    def fixed_mission_estimate(self, lookahead_time_span):

        # make sure there are drones available
        if not hasattr(self, "drones"):
            raise RuntimeError("drone variable has not been initialized.")
        if len(self.drones) <= 0:
            raise RuntimeError("drone variable is empty. Please add drones to the mission planner.")
        
        # initialize the estimated signal
        self.estimated_signal = Signal()

        
        # record the original step
        current_execution_signal_element_data = dict()
        
        for drone in self.drones:
            # current_x = drone.get_x_cor()
            # current_y = drone.get_y_cor()

            current_execution_signal_element_data[drone.get_identifier()] = {"current_coord": drone.get_current_coord()}

        # steps = 0
        current_execution_signal_element_data = Signal_Element(0, current_execution_signal_element_data)

        # append the initial signal to the current estimate signal 
        self.estimated_signal.add(current_execution_signal_element_data)

        # print("type of added: " + str(type(current_execution_signal_element_data)))
        # self.estimated_signal.add(Signal_Element(0, current_execution_signal_element_data))


        # copy the lookahead time span to the steps
        steps = 1
        total_steps = lookahead_time_span

        # enter the execution loop
        while steps <= total_steps:
            # intialize response_data to a dictionary
            # re-initialize everytime the loop runs
            # response_data = dict()
            shared_flight_data = Shared_Flight_Data()

            ##### execution time #####
            for drone in self.drones:
                # debugger
                # drone.get_internal_map().visualize_visited_map()

                # execute the next step of the drone movement
                drone.next_step()

                # emit response data after each execution
                # note that it is crucial to make identifiers unique to appropriately receive the response data
                # response_data = {"Ego": ... "Enemy": ...}
                # response_data[drone.get_identifier()] = drone.emit_response_data()
                shared_flight_data.add(drone.emit_flight_data())
            ##### /execution time #####
             


            ##### data processing #####
            # write the step data to the response_data
            # response_data["step"] = steps

            # create flight data for air traffic control
            ATC_flight_data = ATC_Flight_Data("ATC", {"step": steps})

            # add the flight broadcaster to the 
            shared_flight_data.add(ATC_flight_data)

            

            # generate/append to the estimated signal
            # convert the response data to the format of signal
            current_execution_signal_element_data = dict()

            for drone in self.drones:
                # current_x = response_data[drone.get_identifier()]["current_map_cell"].x()
                # current_y = response_data[drone.get_identifier()]["current_map_cell"].y()
                current_coord = shared_flight_data.get(drone.get_id()).get_map_cell().get_coord()
                # current_execution_signal_element_data[drone.get_identifier()] = {"current_coords": {"x_cor": current_x, "y_cor": current_y}}
                current_execution_signal_element_data[drone.get_identifier()] = {"current_coord": current_coord}

            current_execution_signal_element_data = Signal_Element(steps, current_execution_signal_element_data)
            # self.estimated_signal.add(Signal_Element(steps, current_execution_signal_element_data))
            self.estimated_signal.add(current_execution_signal_element_data)

            # increment the step
            steps += 1
            ##### /data processing #####


            ##### post-execution time #####
            # broadcast the response data back to the drones
            for drone in self.drones:
                # drone.receive_response_data(response_data)
                drone.receive_shared_flight_data(shared_flight_data)

            ##### /post-execution time #####

    def get_signal_estimation(self):
        # function to return the generated estimated signal
        if hasattr(self, "estimated_signal"):
            return self.estimated_signal
        else:
            raise RuntimeError("estimated_signal variable has not been initialized.")
    
# class to support the specification of signal temporal logic
# class STL:
#     pass
#     def evaluate_boundary_robustness(self, signal, map_width, map_height, start_time=0):
#         min_distance = 21
#         for time in range(0, signal.length()):
#             current_x = signal.get_signal_data_by_time(time)["Ego"]["current_coords"]["x_cor"]
#             current_y = signal.get_signal_data_by_time(time)["Ego"]["current_coords"]["y_cor"]
#             if min_distance > distance_to_boundary(current_x, current_y, map_width, map_height):
#                 min_distance = distance_to_boundary(current_x, current_y, map_width, map_height)
#     def evaluate_

# signal = {time/step t0: {...exec data: enemy_loc, ego_loc, future: enemy_speed, ego_speed...}, t1: {...exec data...}, ...}
# signal = {Signal_Element_1, Signal_Element_2}
# signal is a set of Signal_Element indexed (key) by the time
#
# Sample Signal Data
# {
#   0: {'Ego': {'current_coord': (0, 20)}, 'Enemy': {'current_coord': (0, 5)}})
#   ,
#   1: {'Ego': {'current_coord': (0, 20)}, 'Enemy': {'current_coord': (0, 5)}})
#   ...
#}

# signal is simply a list of Signal_Elements
# each time matches to a Signal_Elements object
class Signal:
    def __init__(self):
        # initialize the signal list
        self.signal_list = dict()

    def length(self):
        return len(self.signal_list)

    # slight variation. Signal is a dictionary index by the time associated with the signal element
    def add(self, signal_element):
        # self.signal_list[signal_element.get_time()] = signal_element.get_signal_data()
        self.signal_list[signal_element.get_time()] = signal_element

    def get_signal_data_by_time(self, time):
        return self.signal_list[time].get_signal_data()

    def get_signal_element(self, time):
        # print("type: ", type(self.get_signal_data_by_time(time)))
        # return Signal_Element(time, self.get_signal_data_by_time(time))
        return self.signal_list[time]
        
    # def get_signal_by_time(self, time):
    #     """function that returns a singleton signal"""
    #     new_signal = Signal()

    #     return Signal()
    
    # use ordered list instead in the future
    def __str__(self):
        time_list = self.signal_list.keys()

        str_builder = "{\n"

        # sort the time
        for time in range(0, len(self.signal_list)):
            str_builder += "\t(" + str(time) + ", " + "(" + str(self.signal_list[time]) + ")\n"

        str_builder += "}\n"
        return str_builder

# time/step t0: {...exec data: enemy_loc, ego_loc, 
# support nested data
# 
# Sample Signal Element:
# self.time = 0, 
# self.signal_data = {'Ego': {'current_coord': (0, 20)}, 'Enemy': {'current_coord': (0, 5)}})
class Signal_Element:
    def __init__(self, time, signal_data=dict()):
        self.time = time
        self.signal_data = signal_data

    def get_time(self):
        return self.time

    def get_signal_data(self):
        if hasattr(self, "signal_data"):
            return self.signal_data
        else:
            raise RuntimeError("signal_data variable has not been initialized.")

    def get_signal_data_by_id(self, drone_identifier):
        if hasattr(self, "signal_data"):
            if (drone_identifier in self.signal_data.keys()):
                return self.signal_data[drone_identifier]
            else:
                raise RuntimeError("signal_data variable does not have key: " + drone_identifier)
        else:
            raise RuntimeError("signal_data variable has not been initialized.")
    
    def get_signal_data_by_id_key(self, drone_identifier, key):
        if hasattr(self, "signal_data"):
            if (drone_identifier in self.signal_data.keys()):
                if (key in self.signal_data[drone_identifier].keys()):
                    return self.signal_data[drone_identifier][key]
                else:
                    raise RuntimeError("signal_data[" + drone_identifier + "] variable does not have key: " + key)
            else:
                raise RuntimeError("signal_data variable does not have key: " + drone_identifier)
        else:
            raise RuntimeError("signal_data variable has not been initialized.")

    def __repr__(self):
        return str(self.signal_data)

    def __str__(self):
        return str(self.signal_data)

# support the evaluation of robustness value with respect to a signal
class Robustness:
    def __init__(self, stl_formula, signal):
        self.stl_formula = stl_formula
        self.signal = signal
    
    def evaluate(self):
        # evalute the robustness value with respect to the STL formula and signal given
        return 0
