# Documentation for Feature_Interaction class
# Mon Sep 28 20:28:14 EDT 2020

class Map_Cell
  - Purpose: primitive building block for the map

  - Class Variables:
    - x_cor
      - x coordinate of the system

    - y_cor
      - y coordinate of the system

    - output
      - the output for the robustness map

    - attributes
      - A Python dictionary ({}) that stores key value pairs

  - Member Functions:
    - get_x_cor()

    - get_y_cor()

    - set_output()

    - get_output()

    - set_attribute(key, value)
      - set the attribute dictionary for the map cell given key-value pairs

    - get_attribute(key)
      - get the attribute by the key



class Map
  - Purpose: stores a 1D array of Map_Cell, and the parameters for the map

  - Class Variables:
    - width
    - height
    - internal_map

  - Member Functions:
    - get_width()

    - get_height()

    - get_map_cell(x_index, y_index)

    - set_output(self, x_index, y_index, output)

    - get_output(self, x_index, y_index)

    - get_output_map()

    - visualize_internal_map()

    - visualize_output_map()

    - find_neighbors_8(map_cell)
      - get all 8 neighbors surrounding the current map cell (map_cell)

class Feature_Interaction
  - Purpose: perform the flight mission using maps, drones, barriers and obstacles