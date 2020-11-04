# https://docs.python.org/2/library/unittest.html

import unittest
import tools
import main

class Test_Tools(unittest.TestCase):

    def test_string_builder(self):
        sb = tools.String_Builder()
        sb.append("hello")
        self.assertEqual(str(sb), "hello")
    
    # # initialization of Map_Cell without attributes
    # def test_map_cell_init_without_attributes(self):
    #     map_cell = Map_Cell(Coord(5, 20))

    #     self.assertEqual(str(map_cell), "(5, 20) : 0")

    # def test_set_attribute(self):
    #     map_cell = Map_Cell(Coord(5, 20))
    #     map_cell.set_attribute("visited", True)

    #     self.assertEqual(str(map_cell), "(5, 20) : 0")
    #     self.assertEqual(map_cell.get_attribute("visited"), True)

class Program_Tests(unittest.TestCase):
    def test_print_stmt(self):
        program = """

        // 2020-11-03 20:24:09
        // Simon Chu

        // println with semicolon
        println 1;
        println 1.0;
        println true;
        println "hello, world!";
        println false;

        // println without semicolon
        println 1
        println 1.0
        println true
        println false
        println "hello, world!"

        // print with semicolon
        print 1;
        print 1.0;
        print true;
        print false;
        print "hello, world!";

        // print without semicolon
        print 1
        print 1.0
        print true
        print false

        """

        main.Interpreter.interpret(program)
        
if __name__ == '__main__':
    unittest.main()