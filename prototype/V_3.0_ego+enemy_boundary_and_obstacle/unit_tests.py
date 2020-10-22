# https://docs.python.org/2/library/unittest.html

import unittest
from map_utils import Map_Cell, Map, Coord
from algorithms import Algorithms

class Test_Map_Cell_Methods(unittest.TestCase):

    # initialization of Map_Cell without attributes
    def test_map_cell_init_without_attributes(self):
        map_cell = Map_Cell(Coord(5, 20))

        self.assertEqual(str(map_cell), "(5, 20) : 0")

    def test_set_attribute(self):
        map_cell = Map_Cell(Coord(5, 20))
        map_cell.set_attribute("visited", True)

        self.assertEqual(str(map_cell), "(5, 20) : 0")
        self.assertEqual(map_cell.get_attribute("visited"), True)

class Test_Map_Methods(unittest.TestCase):
    
    # def test_attribute(self):
    #     map = main.Map(10, 20)
    #     map.get_map_cell(5, 5).set_attribute("visited", True)
    #     self.assertEqual(map.get_map_cell(5, 5).get_attribute("visited"), True)
    #     self.assertEqual(map.get_map_cell(5, 6).get_attribute("visited"), False)
    
    def test_attribute2(self):
        map_cell_1 = Map_Cell(Coord(10, 20))
        map_cell_2 = Map_Cell(Coord(20, 10))

        map_cell_1.set_attribute("visited", True)

        self.assertEqual(map_cell_1.get_attribute("visited"), True)
        self.assertEqual(map_cell_2.has_attribute("visited"), False)
        li = []
        li.append(map_cell_1)
        li.append(map_cell_2)
        
        self.assertEqual(li[0].get_attribute("visited"), True)
        self.assertEqual(li[1].has_attribute("visited"), False)

class Test_Algorithm_Methods(unittest.TestCase):
    def test_min_distance_to_boundary(self):
        # create a 21x21 map
        internal_map = Map(21, 21)

        min_distance_1 = Algorithms.min_distance_to_boundary(Coord(5, 5), internal_map)
        min_distance_2 = Algorithms.min_distance_to_boundary(Coord(11, 12), internal_map)

        self.assertEqual(min_distance_1, 5)
        self.assertEqual(min_distance_2, 8)


    def test_distance_between_2_points(self):
        # test 勾三股四弦五
        coord_1 = Coord(0, 0)
        coord_2 = Coord(3, 4)
        distance = Algorithms.distance_between_2_points(coord_1, coord_2)
        self.assertEqual(distance, 5)

if __name__ == '__main__':
    unittest.main()