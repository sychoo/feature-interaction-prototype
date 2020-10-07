# https://docs.python.org/2/library/unittest.html

import unittest
import main

class Test_Map_Cell_Methods(unittest.TestCase):

    # initialization of Map_Cell without attributes
    def test_map_cell_init_without_attributes(self):
        map_cell = main.Map_Cell(5, 20)

        self.assertEqual(str(map_cell), "(5, 20) : 0")

    # def test_map_cell_init_with_attributes(self):
    #     map_cell = main.Map_Cell(5, 20, {"visited": True})

    #     self.assertEqual(str(map_cell), "(5, 20) : 0")
    #     self.assertEqual(map_cell.get_attribute("visited"), True)

    # def test_map_cell_init_with_attributes(self):
    #     map_cell = main.Map_Cell(5, 20, {"visited": True})

    #     self.assertEqual(map_cell.has_attribute("visited"), True)
    #     self.assertEqual(map_cell.has_attribute("hello"), False)

    #     map_cell_2 = main.Map_Cell(5, 21)
    #     self.assertEqual(map_cell_2.has_attribute("visited"), False)

    def test_set_attribute(self):
        map_cell = main.Map_Cell(5, 20)
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
        map_cell_1 = main.Map_Cell(10, 20)
        map_cell_2 = main.Map_Cell(20, 10)

        map_cell_1.set_attribute("visited", True)

        self.assertEqual(map_cell_1.get_attribute("visited"), True)
        self.assertEqual(map_cell_2.has_attribute("visited"), False)
        li = []
        li.append(map_cell_1)
        li.append(map_cell_2)

        
        self.assertEqual(li[0].get_attribute("visited"), True)
        self.assertEqual(li[1].has_attribute("visited"), False)
if __name__ == '__main__':
    unittest.main()