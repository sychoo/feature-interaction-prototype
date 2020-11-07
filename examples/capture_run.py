import subprocess
value = subprocess.check_output("../src/STL_Interpreter/interp ../src/STL_Interpreter/test_suite/print.stls", shell=True)
print(value)
