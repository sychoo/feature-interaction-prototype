# map_utils.py
# support map objects, including map cells and map
# Tue Oct  6 22:28:12 EDT 2020
# Designed with ❤️ by Simon Chu

import math

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

    def distance_to(self, map_cell):
        return math.sqrt((map_cell.get_x_cor() - self.get_x_cor())**2 + (map_cell.get_y_cor() - self.get_y_cor())**2)

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

    def get_diagonal_length(self):
        return math.sqrt(self.width**2 + self.width**2)

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


