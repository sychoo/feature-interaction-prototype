import io
from contextlib import redirect_stdout
import sys
f = io.StringIO()

with redirect_stdout(f):
    sys.stdout.write("hello, world")
    print('foobar')
    print(12)

# print('Got stdout: "{0}"'.format(f.getvalue()))
