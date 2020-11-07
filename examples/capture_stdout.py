import sys
from IPython.utils.capture import capture_output

with capture_output() as c:
    sys.stdout.write('some output\n')

c()

print(c.stdout)
