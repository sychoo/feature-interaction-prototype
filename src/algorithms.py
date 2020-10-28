# algorithms.py
# file to provide algorithm support

# Mon Oct 26 21:45:02 EDT 2020
# Designed with ❤️ by Simon Chu

# include calculating the min distance from the coordinate (x, y) to the boundary (for rectangular map)
# include calculating the distance between the ego drone and the enemy drone
# to-do refactor the code from flight.py to use the algorithms here

import math
# from map_utils import Coord # note that coords cannot be imported because of circular import

class Algorithms:
    """provide algorithm support to prevent repetitive definition of trivial algorithms
    """
    @staticmethod
    def min_distance_to_boundary(coord, internal_map):
        """calculate the minimum distance between a coordinate and the boundary of a 2D map

        Args:
            coord (Coord): the 2D coordinate of a point
            internal_map (Map): the map used to calculate the distance

        Returns:
            int: the minmum distance from the arbitrary point to the boundary of the map
        """
        # calculate the minimum distance to the boundary

        # get the width and height of the map
        map_width = internal_map.get_width()
        map_height = internal_map.get_height()

        # set the boundary of the map
        top_boundary_y = 0
        left_boundary_x = 0
        right_boundary_x = map_width - 1
        bottom_boundary_y = map_height - 1

        # calculate the distance between the coordinates and each of the boundary
        distance_to_top = coord.y() - top_boundary_y
        distance_to_left = coord.x() - left_boundary_x
        distance_to_right = right_boundary_x - coord.x()
        distance_to_bottom = bottom_boundary_y - coord.y()

        # find the minimum distance
        min_distance_to_boundary = min(distance_to_top, distance_to_bottom, distance_to_left, distance_to_right)

        return min_distance_to_boundary

    @staticmethod
    def distance_between_2_points(coord_1, coord_2):
        """calculate the the distance between 2 points

        Args:
            coord_1 (Coord): the first coordinate
            coord_2 (Coord): the second coordinate

        Returns:
            int: the distance between two coordinates
        """
        return math.sqrt((coord_1.x() - coord_2.x()) ** 2 + (coord_1.y() - coord_2.y()) ** 2)
