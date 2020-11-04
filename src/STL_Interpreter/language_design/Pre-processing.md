# Program Pre-processing:
1. Tools.get_raw_program_string/Tools.extract_raw_program_string
    - get rid of all single line new lines within the program
    - if the program doesn't end with a new line, add a new line

2. Lexer class in lexer.py
    - ignore all white spaces other than \n -- new line character (equivalent to \s - \n)
    - ignore all single-line and multi-line comments as well as the white spaces trailing them (so that it won't cause errors)
