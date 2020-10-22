# drone_utils.py
# drone utilities to support drone features

# Tue Oct  6 22:28:12 EDT 2020
# Designed with ❤️ by Simon Chu

import abc
import parser 
from map_utils import Coord

# Drone object works together with the map
# the drone decide for itself where it would like to go next
class Drone(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_step(self):
        # abstract method to execute everytime the drone advances in the execution loop
        pass
    
    @abc.abstractmethod
    def emit_response_data(self):
        # output the response data from the drone
        # abstact method to execute everytime an execution cycle just finished
        pass

    def receive_response_data(self, response_data):
        # receive response data from the broadcaster in the execution loop
        self.response_data = response_data

    def has_response_data(self):
        # check whether response data is initialized
        return hasattr(self, "response_data")

    def get_response_data(self):
        # fetch the response data received from the broadcaster in the run method in the MissionPlanner
        if hasattr(self, "response_data"):
            return self.response_data
        else:
            raise RuntimeError("response_data variable has not been initialized.")

    def init_attribute(self):
        # initialize the attribute
        # can hold various things like flight path list of tuple of coordinates, 
        self.attributes = dict()

    def set_identifier(self, identifier):
        # set identifier for the drone
        self.identifier = identifier

    def get_identifier(self):
        # get the identifier for the drone
        if hasattr(self, "identifier"):
            return self.identifier
        else:
            raise RuntimeError("drone identifier variable has not been initialized.")

    def set_internal_map(self, internal_map):
        # set the internal map associated with the drone
        self.internal_map = internal_map

    def get_internal_map(self):
        if hasattr(self, "internal_map"):
            return self.internal_map
        else:
            raise RuntimeError("map variable has not been initialized.")

    def set_initial_location(self, init_x_cor, init_y_cor):
        # set the initial position coordinates for the drone
        self.init_x_cor = init_x_cor
        self.init_y_cor = init_y_cor

        # when setting the initial value, the current location will be automatically set to the intial values
        self.set_current_location(init_x_cor, init_y_cor)

    def get_init_x_cor(self):
        # get the initial X coordinate
        return self.init_x_cor
    
    def get_init_y_cor(self):
        # get the initial Y coordinate
        return self.init_y_cor

    def set_current_location(self, x_cor, y_cor):
        # set the current location for the drone
        self.x_cor = x_cor
        self.y_cor = y_cor

    def get_current_location(self):
        # obtain the current drone location
        return (self.x_cor, self.y_cor)
    
    def get_current_location_map_cell(self):
        # get the map_cell object of the current location
        # first ensure that the map variable is set
        if hasattr(self, "internal_map"):
            return self.internal_map.get_map_cell(Coord(self.x_cor, self.y_cor))
        else:
            raise RuntimeError("map variable has not been initialized.")

    def get_x_cor(self):
        return self.x_cor
    
    def get_y_cor(self):
        return self.y_cor

    def __str__(self):
        return self.get_identifier() + " Drone: (" + self.get_x_cor() + ", " + self.get_y_cor() + ")" 

    def __repr__(self):
        return self.get_identifier() + " Drone: (" + self.get_x_cor() + ", " + self.get_y_cor() + ")" 

# EnemyDrone class inherits the Drone parent class
class EnemyDrone(Drone):
    def __init__(self, internal_map):
        self.set_internal_map(internal_map)
        self.set_identifier("Enemy")

    def next_step(self):
        # the next_step of the enemy drone depends on the location of the ego drone
        # it will select the path that will maximally approach the ego drone

        # Note that the response data may not be intialized the first time the cycle executes.
        # the next move of the enemy drone will depend on the previous location of the ego drone
        if self.has_response_data():

            # case when the response data has been received
            response_data = self.get_response_data()

            # get the Map_Cell on the current location
            current_map_cell = self.internal_map.get_map_cell(Coord(self.get_x_cor(), self.get_y_cor()))

            # set the output to 1 (debug, show path)
            current_map_cell.set_output(1)

            # find all neighboring map_cell (neighbor_list {"north": map_cell "south", "east", "west", ...})
            neighbor_dict = self.internal_map.find_neighbors_8(current_map_cell)

            neighbor_map_cells = neighbor_dict.values()

            # warning: this is highly brittle
            # acquire the ego drone x, y coordinates from the response data
            ego_drone_x_cor = response_data["Ego"]["current_x_cor"]
            ego_drone_y_cor = response_data["Ego"]["current_y_cor"]
            ego_drone_map_cell = self.get_internal_map().get_map_cell(Coord(ego_drone_x_cor, ego_drone_y_cor))


            # initialize the min distance to the diagonal length of the map
            # which is the maximum distance you can achieve on the map
            min_ego_enemy_drone_distance = self.get_internal_map().get_diagonal_length()

            # initialize the next map cell by default to current map cell
            next_step_map_cell = current_map_cell

            for neighbor_map_cell in neighbor_map_cells:
                distance_to_ego_drone = neighbor_map_cell.distance_to(ego_drone_map_cell)
                if min_ego_enemy_drone_distance > distance_to_ego_drone:
                    min_ego_enemy_drone_distance = distance_to_ego_drone
                    next_step_map_cell = neighbor_map_cell

            self.set_current_location(next_step_map_cell.x(), next_step_map_cell.y())
            # decision: distance advances (dynamic) vs. distance only (static comparison)
            # find all neighbors
            # check which path can advance the most (maybe restrict to 4 neighbors instead of 8 in the future?)

            
        else:
            # case when the response data is not initialized
            # drone location remain unchanged
            pass

    def emit_response_data(self):
        return {"current_x_cor": self.get_x_cor(), "current_y_cor": self.get_y_cor(), "current_map_cell": self.get_current_location_map_cell()}

# EgoDrone class inherits the Drone parent class
class EgoDrone(Drone):
    # initialize the ego drone with internal map
    def __init__(self, internal_map):
        self.set_internal_map(internal_map)
        self.set_identifier("Ego")

        # set the mission of the EgoDrone
        # self.fly_x_squared

    def next_step(self):
        # print("hello")

        # get the Map_Cell on the current location
        current_map_cell = self.internal_map.get_map_cell(Coord(self.get_x_cor(), self.get_y_cor()))
        # print(current_map_cell)
        # mark current map cell
        current_map_cell.set_output(1)

        # mark the visited attribute in the map cell as true
        current_map_cell.set_attribute("visited", True)

        # compute the dynamic robustness for all cells based on the location of the drone
        # self.compute_dynamic_robustness(current_map_cell)

        # find all neighboring map_cell (neighbor_list {"north": "south", "east", "west", ...})
        neighbor_dict = self.internal_map.find_neighbors_8(current_map_cell)

        # find the next cell, using the initial coordinates, since graph has to be based on the intial x and y coordinates
        current_map_cell = self.find_next_map_cell_fly_x_squared(neighbor_dict, self.get_init_x_cor(), self.get_init_y_cor())
        
        # set the current location to the new location
        self.set_current_location(current_map_cell.x(), current_map_cell.y())

    def emit_response_data(self):
        return {"current_x_cor": self.get_x_cor(), "current_y_cor": self.get_y_cor(), "current_map_cell": self.get_current_location_map_cell()}

    # def create_drone("ego/enemy", tuple of initial position on the map, map_object)
    # check if the initial position is valid on the map
    # debugging
    # return a map cell
    def find_next_map_cell_fly_x_squared(self, neighbor_dict, init_x_cor, init_y_cor):
        # graph_length : map_length
        graph_to_map_ratio = 2/self.internal_map.get_width() # the ratio between the graph (mathematical formula) to the discretized map (cell length counts as 1)

        # encode the precedence rule to resolve the direction to fly to when the score is the same
        precedence = ["east", "southeast", "south", "southwest", "west", "northwest", "north", "northeast"]

        formula = "x**2"
        formula_parsed = parser.expr(formula).compile()

        # check whether the cell is visited already, if so, don't visit,
        # if not, check close proximity to the graph using the formula
        # debug "flyeight-visited"
        min_diff = 1

        # {"map_cell": diff value...}
        map_cell_displacement_diff = {}

        # compute the lowest diff in the neighbor_dict
        for key in neighbor_dict.keys():
            # get the current neighbor map cell
            current_map_cell = neighbor_dict[key]

            # print("checking" + str(current_map_cell))

            # ensure that the cell is not yet visited
            # if current_map_cell.has_attribute("visited") and current_map_cell.get_attribute("visited"):
            # print(current_map_cell.get_attribute_dict())

            # debug, flip the guard below to make it work
            if current_map_cell.has_attribute("visited") and current_map_cell.get_attribute("visited"):
            # if current_map_cell.get_output() == 1:
                # print("Cell " + str(current_map_cell) + " is visited")
                pass

            else:
                # compute the x coordinate displacement from the origin
                x_cor_displacement = current_map_cell.x() - init_x_cor

                # compute the x displacement on the graph from the origin
                x_graph_displacement = x_cor_displacement * graph_to_map_ratio

                # assign x value in formula
                x = x_graph_displacement

                # evaluate the formula
                y_graph_displacement = eval(formula_parsed) 
                # print(y_graph_displacement)

                # compute the y coordinate displacement from the origin
                y_cor_displacement = y_graph_displacement / graph_to_map_ratio

                # compute the actual y coordinate displace from the current map cell
                actual_y_cor_displacement = current_map_cell.y() - init_y_cor

                # compute the difference in displacement
                current_diff = abs(y_cor_displacement + actual_y_cor_displacement)

                map_cell_displacement_diff[current_map_cell] = (key, current_diff)
        
        #map_cell_displacement_diff
        #{"map_cell": ("north", displacement_diff)}

        # sorting the displacement_diff dictionary by its values (ascending order)
        sorted_displacement_diff = sorted(map_cell_displacement_diff.items(), key=lambda x: x[1][1])
        
        #[(map_cell, (north, displacement_diff)), (...)]
        min_diff_value = sorted_displacement_diff[0][1][1]
        # sorted_displacement_diff is sorted by displacement_diff

        same_displacement_diff_value_dict = {}

        for i in sorted_displacement_diff:
            if i[1][1] == min_diff_value:
                same_displacement_diff_value_dict[i[1][0]] = i[0]

        # same_displacement_diff_value_dict
        # {"north": map_cell}

        # work on precedence
        for direction in precedence:
            if direction in same_displacement_diff_value_dict.keys():
                # print("Selected " + direction)
                return same_displacement_diff_value_dict[direction]
        # print(sorted_displacement_diff)

        
        # return sorted_displacement_diff[0][0]

