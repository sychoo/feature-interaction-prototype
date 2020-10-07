# Designed by Simon Chu
# Thu Sep 24 16:01:06 EDT 2020

# imported modules
import parser # for parsing the mathematical formulas
import math # for math calculations
import statistics # for statistical analysis (mean, variance, etc)
import numpy as np # numpy for array generations

# seaborn visualization library
import seaborn as sns
sns.set_theme()
import matplotlib.pyplot as plt



# Drone object works together with the map
class Drone:
    def __init__(self, identifier):
        self.identifier = identifier

    def set_location(self, x_cor, y_cor):
        self.x_cor = x_cor
        self.y_cor = y_cor

    def get_location(self):
        return (self.x_cor, self.y_cor)
    
    def get_x_cor(self):
        return self.x_cor
    
    def get_y_cor(self):
        return self.y_cor

# Map_Cell object is instantiated on the map
class Map_Cell:
    def __init__(self, x_cor, y_cor):
        # stores the x and y coordinates corresponding to each cell
        self.x_cor = x_cor
        self.y_cor = y_cor

        self.attributes = dict() # Python dictionary, stores different attribute/property about the heatmap cells
        self.output = 0 # specical variable to specify the value output to the heatmap. Initialized to 0 by default
    
    # check whether the map_cell has the attribute
    def has_attribute(self, key):
        return key in self.attributes

    # set attribute for the cell
    def set_attribute(self, key, value):
        self.attributes[key] = value
    
    # get attribute for the cell
    def get_attribute(self, key):
        return self.attributes[key]

    def get_attribute_dict(self):
        return self.attributes
        # print(str(self.attributes))

    # get x_cor for the cell
    def get_x_cor(self):
        return self.x_cor
    
    # get y_cor for the cell
    def get_y_cor(self):
        return self.y_cor

    # set the output for the heatmap
    def set_output(self, output):
        self.output = output
    
    # get the output specified for the map cell
    def get_output(self):
        return self.output

    def __str__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ") : " + str(self.output)

    def __repr__(self):
        return "(" + str(self.x_cor) + ", " + str(self.y_cor) + ") : " + str(self.output)



# Map object represent the map, and consist of a list of Map_Cells
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # initialize a 1-D array that contains MapCells
        self.internal_map = []

        # this data structure flattens the 2D array to 1D, from left to right (increment x_cor, then increment y_cor)
        for y in range(height):
            for x in range(width):
                new_map_cell = Map_Cell(x, y)
                self.internal_map.append(new_map_cell)

        # debug
        # for i in self.internal_map:
        #     print("(" + str(i.get_x_cor()) + " , " + str(i.get_y_cor()) + ")")
            
        # print(self.internal_map)

    def get_flattened_internal_map(self):
        if hasattr(self, "internal_map"):
            return self.internal_map
        else:
            raise RuntimeError("map variable has not been initialized.")

    def get_output(self, x_index, y_index):
        return self.get_map_cell(x_index, y_index).get_output()

    def set_output(self, x_index, y_index, output):
        self.get_map_cell(x_index, y_index).set_output(output)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height

    def get_map_cell(self, x_index, y_index):
        # check the range for the x and y index
        if self.check_index_bound(x_index, y_index):
            pass
        else:
            raise RuntimeError("index out of bound, unable to obtain map cell")

        # translate 2D array index to flattened 1D array index
        transformed_index = y_index * self.width + x_index
        return self.internal_map[transformed_index]

    def check_index_bound(self, x_index, y_index):
        # check whether the x and y index is within the bound of the map
        return x_index >= 0 and x_index < self.width and y_index >= 0 and y_index < self.height

    def get_output_map(self):
        # generate the output map for seaborn (after manipulating the special output variable)
        return [ [ self.get_map_cell(x, y).get_output() for x in range(self.width) ] for y in range(self.height) ]

    def find_neighbors_8(self, map_cell):
        neighbor_dict = {}

        x_cor = map_cell.get_x_cor()
        y_cor = map_cell.get_y_cor()

        new_x_cor = x_cor
        new_y_cor = y_cor - 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["north"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor
        new_y_cor = y_cor + 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["south"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor + 1
        new_y_cor = y_cor
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["east"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor - 1
        new_y_cor = y_cor
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["west"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor + 1
        new_y_cor = y_cor - 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["northeast"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor + 1
        new_y_cor = y_cor + 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["southeast"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor - 1
        new_y_cor = y_cor + 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["southwest"] = self.get_map_cell(new_x_cor, new_y_cor)

        new_x_cor = x_cor - 1
        new_y_cor = y_cor - 1
        if self.check_index_bound(new_x_cor, new_y_cor):
            neighbor_dict["northwest"] = self.get_map_cell(new_x_cor, new_y_cor)

        return neighbor_dict

    def visualize_internal_map(self):
        # visualize the internal maps (containing x and y coordinate and the output value)

        # check whether the internal_map attribute has been initialized in the Map object
        if hasattr(self, "internal_map"):
            for index, map_cell in enumerate(self.internal_map):
                if index % self.width == 0:
                    print("height = " + str(map_cell.get_y_cor()))

                print(map_cell)

                if index % self.width == self.width - 1:
                    print()
        else:
            raise RuntimeError("map variable has not been initialized.")

    def visualize_output_map(self):
        # visualize the map if the map contains "map" attribute
        for row_array in self.get_output_map():
            print("\t", end="")

            for element in row_array:
                print("{0:2}".format(element), end="")

            print()






# main object for Feature Interaction problem
class Feature_Interaction:
    def __init__(self):
        pass
    
    # round the float value to the nearest integer value
    def round(self, float_value):
        return int(float_value + 0.5)

    def create_internal_map(self, width, height):
        self.internal_map = Map(width, height)

    def get_internal_map(self):
        if hasattr(self, "internal_map"):
            return self.internal_map
        else:
            raise RuntimeError("map variable has not been initialized.")

    # def create_drone("ego/enemy", tuple of initial position on the map, map_object)
    # check if the initial position is valid on the map
    # debugging
    def find_next_map_cell_fly_x_squared(self, neighbor_dict, init_x_cor, init_y_cor):
        # graph_length : map_length
        graph_to_map_ratio = 2/self.internal_map.get_width() # the ratio between the graph (mathematical formula) to the discretized map (cell length counts as 1)

        # encode the precedence
        precedence = ["east", "southeast", "south", "southwest", "west", "northwest", "north", "northeast"]

        # minus_one = ["west", "northwest", "southwest"]
        # plus_one = ["east", "northeast", "southeast"]
        # constant = ["north", "south"]

        # coded Lemniscate formulas

        formula_1 = "x**2"
        #fly 8
        # formula_1 = "math.sqrt(-x**4 + x**2)" # y >= 0
        # formula_2 = "-math.sqrt(-x**4 + x**2)" # y < 0

        formula_1_parsed = parser.expr(formula_1).compile()
        # formula_2_parsed = parser.expr(formula_2).compile()

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
                x_cor_displacement = current_map_cell.get_x_cor() - init_x_cor

                # compute the x displacement on the graph from the origin
                x_graph_displacement = x_cor_displacement * graph_to_map_ratio

                # assign x value in formula
                x = x_graph_displacement

                # evaluate the formula
                y_graph_displacement = eval(formula_1_parsed) 
                # print(y_graph_displacement)

                # compute the y coordinate displacement from the origin
                y_cor_displacement = y_graph_displacement / graph_to_map_ratio

                # compute the actual y coordinate displace from the current map cell
                actual_y_cor_displacement = current_map_cell.get_y_cor() - init_y_cor

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

    def fly_x_squared(self, init_x_cor, init_y_cor):

        # the origin of the graph is the initial position of the graph
        # origin_x = x_cor
        # origin_y = y_cor

        # get the starting cell
        current_map_cell = self.internal_map.get_map_cell(init_x_cor, init_y_cor)

        # set the number of steps
        steps = 23
        # current_x_offset = 0 # offset of x relative to the origin


        while steps >= 0:
            # mark current map cell
            current_map_cell.set_output(1)
            # print(current_map_cell)

            # mark the visited attribute in the map cell as true
            current_map_cell.set_attribute("visited", True)

            # compute the dynamic robustness for all cells based on the location of the drone
            self.compute_dynamic_robustness(current_map_cell)

            # find all neighboring map_cell (neighbor_list {"north": "south", "east", "west", ...})
            neighbor_dict = self.internal_map.find_neighbors_8(current_map_cell)
            # print(neighbor_dict)

            # find the next cell
            current_map_cell = self.find_next_map_cell_fly_x_squared(neighbor_dict, init_x_cor, init_y_cor)
            
            steps -= 1


    # compute the static robustness of the map based on obstacles and boundaries
    # right now boundaries only
    # compute it for all cells
    def compute_static_robustness(self):
        # set the minimum safety distance to the boundary
        min_safety_distance_boundary = 3.0

        # parameter for robustness score penalization
        alpha = 32

        # compute min and max robustness for scaling
        # maybe adjust the min/max robustness score to the actual min/max robustness score in the future
        # robustness_min = -1 * min_safety_distance_boundary
        # robustness_max = max(self.internal_map.get_width(), self.internal_map.get_height()) / 2 - 1

        # set the boundary of the map
        top_boundary_y = 0
        left_boundary_x = 0
        right_boundary_x = self.internal_map.get_width() - 1
        bottom_boundary_y = self.internal_map.get_height() - 1

        # store the raw robustness values for analyzing min and max robustness
        raw_robustness_value_list = []

        # first robustness loop. Calculate the raw robustness score
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            x_cor = map_cell.get_x_cor()
            y_cor = map_cell.get_y_cor()

            distance_to_top = y_cor - top_boundary_y
            distance_to_bottom = bottom_boundary_y - y_cor
            distance_to_left = x_cor - left_boundary_x
            distance_to_right = right_boundary_x - x_cor

            min_distance_to_boundary = min(distance_to_top, distance_to_bottom, distance_to_left, distance_to_right)

            raw_robustness_value = min_distance_to_boundary - min_safety_distance_boundary

            raw_robustness_value_list.append(raw_robustness_value)

            # store the raw robustness value to the map cell for future analysis
            map_cell.set_attribute("static_robustness_score_raw", raw_robustness_value)



        # compute the min and max robustness scores
        robustness_min = min(raw_robustness_value_list)
        robustness_max = max(raw_robustness_value_list)



        # second loop, scale and penalize robustness scores
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            raw_robustness_value = map_cell.get_attribute("static_robustness_score_raw")

            # scale the robustness value to a scale of -1 to 1 (inclusive)
            scaled_robustness_value = 0

            if raw_robustness_value < 0:
                scaled_robustness_value = (raw_robustness_value - robustness_min) / (-1 * robustness_min) - 1
            else:
                scaled_robustness_value = raw_robustness_value / robustness_max

            # penalize negative robustness scores
            penalized_robustness_value = 0

            if raw_robustness_value < 0:
                penalized_robustness_value = raw_robustness_value - (alpha**(-raw_robustness_value - 1)/(alpha - 1))
            else:
                penalized_robustness_value = raw_robustness_value
            
            map_cell.set_attribute("static_robustness_score_scaled", scaled_robustness_value)
            map_cell.set_attribute("static_robustness_score_penalized", penalized_robustness_value)

    # compute the dynamic robustness based on the location of the enemy drone
    # compute it for all cells
    def compute_dynamic_robustness(self, enemy_map_cell):
        alpha = 32

        min_safety_distance_enemy_drone = 3.0

        x_cor_enemy = enemy_map_cell.get_x_cor()
        y_cor_enemy = enemy_map_cell.get_y_cor()

        # robustness_value = 0

        # robustness_min = -1 * min_safety_distance_enemy_drone
        # robustness_max = max(self.internal_map.get_width(), self.internal_map.get_height()) / 2 - 1

        # store the raw robustness values
        raw_robustness_value_list = []

        for map_cell in self.get_internal_map().get_flattened_internal_map():
            x_cor = map_cell.get_x_cor()
            y_cor = map_cell.get_y_cor()

            distance_to_enemy_drone = math.sqrt((x_cor - x_cor_enemy)**2 + (y_cor - y_cor_enemy)**2)
            raw_robustness_value = distance_to_enemy_drone - min_safety_distance_enemy_drone

            # by default set to empty list []
            original_dynamic_robustness_score_raw = []
            if (map_cell.has_attribute("dynamic_robustness_score_raw")):
                original_dynamic_robustness_score_raw = map_cell.get_attribute("dynamic_robustness_score_raw")

            # store the list of raw robustness scores in the map cell
            original_dynamic_robustness_score_raw.append(raw_robustness_value)
            map_cell.set_attribute("dynamic_robustness_score_raw", original_dynamic_robustness_score_raw)

            # append the robustness value to the list
            raw_robustness_value_list.append(raw_robustness_value)



        # compute the max and min robustness value
        robustness_max = max(raw_robustness_value_list)
        robustness_min = min(raw_robustness_value_list)



        for map_cell in self.get_internal_map().get_flattened_internal_map():
            # obtain the raw robustness value from the map cell
            raw_robustness_value = map_cell.get_attribute("dynamic_robustness_score_raw")[-1]

            original_dynamic_robustness_score_scaled = []
            if (map_cell.has_attribute("dynamic_robustness_score_scaled")):
                original_dynamic_robustness_score_scaled = map_cell.get_attribute("dynamic_robustness_score_scaled")
            
            original_dynamic_robustness_score_penalized = []
            if (map_cell.has_attribute("dynamic_robustness_score_penalized")):
                original_dynamic_robustness_score_penalized = map_cell.get_attribute("dynamic_robustness_score_penalized")

            # scale the robustness value
            if raw_robustness_value < 0:
                scaled_robustness_value = (raw_robustness_value - robustness_min) / (-1 * robustness_min) - 1
            else:
                scaled_robustness_value = raw_robustness_value / robustness_max


            # penalize negative robustness scores
            penalized_robustness_value = 0

            if raw_robustness_value < 0:
                penalized_robustness_value = raw_robustness_value - (alpha**(-raw_robustness_value - 1)/(alpha - 1))
            else:
                penalized_robustness_value = raw_robustness_value

            # append the computed values to the corresponding cells
            original_dynamic_robustness_score_scaled.append(scaled_robustness_value)
            original_dynamic_robustness_score_penalized.append(penalized_robustness_value)

            map_cell.set_attribute("dynamic_robustness_score_scaled", original_dynamic_robustness_score_scaled)
            map_cell.set_attribute("dynamic_robustness_score_penalized", original_dynamic_robustness_score_penalized)

    def compute_output(self):
        # use the static robustness score
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # map_cell.set_output(map_cell.get_attribute("static_robustness_score_scaled"))

        # fragmented heat map (a particular state in the process)
        # use the static robustness score
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # map_cell.set_output(map_cell.get_attribute("dynamic_robustness_score_scaled")[23] * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

        # min robustness (without boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_scaled")))

            # penalized
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_penalized")))

        # min robustness (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_scaled")) * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

            # penalized
            # map_cell.set_output(min(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

        # max robustness (without boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_scaled")))

            # penalized
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_penalized")))
        
        # max robustness (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_scaled")) * 0.5 + map_cell.get_attribute("static_robustness_score_scaled") * 0.5)

            # penalized
            # map_cell.set_output(max(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

        # average (without boundary)
        for map_cell in self.get_internal_map().get_flattened_internal_map():
            # scaled
            # map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_scaled")))
            map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_penalized")))
        
        # average (with boundary)
        # for map_cell in self.get_internal_map().get_flattened_internal_map():
            # map_cell.set_output(statistics.mean(map_cell.get_attribute("dynamic_robustness_score_penalized")) * 0.5 + map_cell.get_attribute("static_robustness_score_penalized") * 0.5)

    # display the heatmap using seaborn library
    # use function used in previous program

    # How to draw blank heatmaps?
    # https://seaborn.pydata.org/generated/seaborn.heatmap.html
    def display_heatmap(self):
        data = self.get_internal_map().get_output_map()

        # use zeros like and ones like to display the data
        # mask = np.ones_like(data)
        # mask[np.triu_indices_from(mask)] = True
        # mask[10][1] = False # Do not display 10, 1

        ax = sns.heatmap(data,  cmap="Spectral")
        # ax = sns.heatmap(data, cmap="coolwarm")

        # configure the heatmap interface
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True, length=0)
        plt.show()

    # def get_internal_map(self):
    #     if hasattr(self, "internal_map"):
    #         return self.internal_map
    #     else:
    #         raise RuntimeError("map variable has not been initialized.")

if __name__ == "__main__":
    # Experiment 1
    feature_obj = Feature_Interaction()

    # create a 21 x 21 map
    feature_obj.create_internal_map(21, 21)

    # feature_obj.internal_map.visualize_internal_map()

    

    # set starting position as (0, 20)
    feature_obj.fly_x_squared(0, 20) # center of the map (10, 10)

    # feature_obj.get_internal_map().visualize_internal_map()

    # display the path 
    feature_obj.get_internal_map().visualize_output_map()
    # feature_obj.display_heatmap()

    # compute the static robustness score for map cells
    feature_obj.compute_static_robustness()

    feature_obj.compute_output()

    feature_obj.display_heatmap()

    # Experiment 2
    # map = Map(10, 20)
    # map_cell = map.get_map_cell(5, 10)

    # map.visualize_internal_map()

    # print()
    # print(map_cell)

    # map = Map(5, 2)
    # map_cell = map.get_map_cell(3, 1)

    # map.visualize_internal_map()

    # print()
    # print(map_cell)



    # feature_obj.create_map(20, 20)
    # feature_obj.display_map()
    # print(feature_obj.map)
    # encode flight pattern
    # Map(10, 20).visualize_internal_map()
    # Map(10, 10).visualize_output_map()