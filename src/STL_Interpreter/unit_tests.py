# *** Note that name of the test function must start with "test"

# https://docs.python.org/2/library/unittest.html
import unittest
import tools
import main
import sys
import AST

sys.path.append("AST")
import exceptions # AST/exceptions.py

import subprocess

# https://www.devdungeon.com/content/python-use-stringio-capture-stdout-and-stderr
# from io import StringIO

# for capturing standard output
# from IPython.utils.capture import capture_output

TEST_DIR = "test_suite/"

def test_file_path(test_file):
    """function obtain the file path"""
    return TEST_DIR + test_file

class Test_Tools(unittest.TestCase):

    def test_evaluation_context(self):
        ctx_1 = AST.Eval_Context.get_empty_context()
        ctx_1.add(AST.Id_Val("i"), 10)
        ctx_1.add(AST.Id_Val("j"), 20)
        ctx_1.add(AST.Id_Val("k"), 30)

        ctx_2 = AST.Eval_Context.get_empty_context()
        ctx_2.add(AST.Id_Val("a"), 100)
        ctx_2.add(AST.Id_Val("b"), 200)
        ctx_2.add(AST.Id_Val("c"), 300)

        self.assertEqual(ctx_1.lookup(AST.Id_Val("k")), 30)
        self.assertEqual(ctx_2.lookup(AST.Id_Val("b")), 200)

        # look up something that doesn't exist in the context scope
        try:
            ctx_1.lookup(AST.Id_Val("ds"))
        except exceptions.Context_Lookup_Error as e:
            # flush out the error message so that it doesn't print at the end
            sys.stdout.flush()

        # look up outer scope of top-level context, result in None
        self.assertEqual(ctx_2.get_outer_context_var_id(), None)

    def test_type_context(self):
        ctx_1 = AST.Type_Context.get_empty_context()
        ctx_1.add(AST.Id_Val("i"), 10)
        ctx_1.add(AST.Id_Val("j"), 20)
        ctx_1.add(AST.Id_Val("k"), 30)

        ctx_2 = AST.Type_Context.get_empty_context()
        ctx_2.add(AST.Id_Val("a"), 100, {"val": True})
        ctx_2.add(AST.Id_Val("b"), 200)
        ctx_2.add(AST.Id_Val("c"), 300)

        self.assertEqual(ctx_1.lookup(AST.Id_Val("k")), 30)
        self.assertEqual(ctx_2.lookup(AST.Id_Val("b")), 200)

        # look up something that doesn't exist in the context scope
        try:
            ctx_1.lookup(AST.Id_Val("ds"))
        except exceptions.Context_Lookup_Error as e:
            # flush out the error message so that it doesn't print at the end
            sys.stdout.flush()

        # look up outer scope of top-level context, result in None
        self.assertEqual(ctx_2.get_outer_context_var_id(), None)
    def test_string_builder(self):
        sb = tools.String_Builder()
        sb.append("Hello")
        sb.append(", ")
        sb.append("World")
        sb.append("!")
        self.assertEqual(str(sb), "Hello, World!")


    def test_extract_raw_program_string(self):
        # test when there is NOT a \n at the end
        string = "Hello, \n \n     \n\nWorld!"
        extracted_raw_program_string = tools.Tools.extract_raw_program_string(string)
        expected_string = "Hello, \nWorld!\n"
        self.assertEqual(extracted_raw_program_string, expected_string)
    
        # test when there is a \n at the end
        string = "Hello, \n \n     \n\nWorld!\n"
        extracted_raw_program_string = tools.Tools.extract_raw_program_string(string)
        expected_string = "Hello, \nWorld!\n"
        self.assertEqual(extracted_raw_program_string, expected_string)


    def test_get_raw_program_string(self):
        # test when there is NOT a \n at the end
        test_file = test_file_path("hello.txt")
        raw_program_string = tools.Tools.get_raw_program_string(test_file)
        expected_string = "Hello, \nWorld!\n"
        self.assertEqual(raw_program_string, expected_string)

        # test when there is a \n at the end
        test_file = test_file_path("hello2.txt")
        raw_program_string = tools.Tools.get_raw_program_string(test_file)
        expected_string = "Hello, \nWorld!\n"
        self.assertEqual(raw_program_string, expected_string)


class Program_Tests(unittest.TestCase):
    """class to faciliate the testing of programs
    4 approaches to test programs
    - simply run the program, make sure the program does not raise any exceptions
    - specify the program in the unit test, run the program
    - specify the program in test_suite/ directory, specify the file name the run the program (embedd the program in the unit test)
    """
    test_dir = "test_suite/"
    
    def test_run_program(self):
        """run program without giving expected input. check if error occurs during execution"""
        test_file = test_file_path("print.stl")
        main.Interpreter(test_file)
        sys.stdout.flush()


    def test_unary_arith_op_with_file(self):
        """run program file by shell command, highly depends on interp command"""
        test_file = test_file_path("unary_arith_op.stl")
        actual_output = subprocess.check_output("python3 main.py " + test_file, shell=True)
        expected_output = """-1
-1.0
10
-1
-8.0
"""
        # decode the output to string (byte -> string)
        decoded_actual_output = actual_output.decode()
        self.assertEqual(decoded_actual_output, expected_output)



    def test_val_var_decl_assign_with_file(self):
        """run program file by shell command, highly depends on interp command"""
        test_file = test_file_path("normal_assign.stl")
        actual_output = subprocess.check_output("python3 main.py " + test_file, shell=True)
        expected_output = """10
hello
3.1415926
false
10
hello
3.1415926
false
10
hello
3.1415926
false
10
hello
3.1415926
false
1000
world
6.28
true
10
world
628.0
true
"""
        # decode the output to string (byte -> string)
        decoded_actual_output = actual_output.decode()
        self.assertEqual(decoded_actual_output, expected_output)

    def test_binary_operator_with_file(self):
        """run program file by shell command, highly depends on interp command"""
        test_file = test_file_path("bin_op.stl")
        actual_output = subprocess.check_output("python3 main.py " + test_file, shell=True)
        expected_output = """----- INT -----
2
79
152
0
false
true
false
true
false
true
false
true
false
true
false
true
----- FLOAT -----
2.1
79.0
152.8
0.5
false
true
false
true
false
true
false
true
false
true
false
true
----- LOGICAL -----
false
true
false
true
false
true
"""

        # decode the output to string (byte -> string)
        decoded_actual_output = actual_output.decode()

        self.assertEqual(decoded_actual_output, expected_output)

    def test_print_stmt_with_file(self):
        """run program file by shell command, highly depends on interp command"""
        test_file = test_file_path("print.stl")
        actual_output = subprocess.check_output("python3 main.py " + test_file, shell=True)
        expected_output = """1
1.0
true
hello, world!
false
1
1.0
true
false
hello, world!
11.0truefalsehello, world!11.0truefalse"""

        # decode the output to string (byte -> string)
        decoded_actual_output = actual_output.decode()

        self.assertEqual(decoded_actual_output, expected_output)

    def test_print_stmt_with_program_string(self):
        """run program by specifying the program within the unit test"""
        # execute python script on command line https://stackoverflow.com/questions/5136611/capture-stdout-from-a-script

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

        # extract raw program string
        raw_program_string = tools.Tools.extract_raw_program_string(program)

        # actual_output = subprocess.check_output('python3 -c  import main; main.Interpreter.interpret("""' + raw_program_string + '""");', shell=True)
        #works
        # actual_output = subprocess.check_output('python3 -c \'import main; main.Interpreter.interpret("""print "hello, world";""")\'', shell=True)

        actual_output = subprocess.check_output('python3 -c \'import main; main.Interpreter.interpret("""'+ raw_program_string + '""")\'', shell=True)
        # python3 -c 'import main; main.Interpreter.interpret("""print "hello, world";""")'  
        expected_output = """1
1.0
true
hello, world!
false
1
1.0
true
false
hello, world!
11.0truefalsehello, world!11.0truefalse"""

        # decode the output to string (byte -> string)
        decoded_actual_output = actual_output.decode()

        self.assertEqual(decoded_actual_output, expected_output)


    def test_empty_files_exit_0(self):
        """ensure interpreter doesn't raise errors code != 0 when given an empty file or file with white spaces"""
        file_list = ["empty.stl", "empty_2.stl", "empty_3.stl", "empty_4.stl"]

        for file in file_list:
            try:
                main.Interpreter(test_file_path(file))
            except SystemExit as e:
                # make sure empty program exit with code 0
                self.assertEqual(e.code, 0)



if __name__ == '__main__':
    unittest.main()